## Users & ChatBots API

_OpenAPI: x-bees users service — version 2018-05-10_

**Servers**

- `https://api.x-bees.com` — Production
- `https://api-stable.x-bees.com` — Stable
- `https://api-stage.x-bees.com` — Stage

### Deprecated

#### `POST` `/v2/users/BatchGetUsersPbxLinkData`

Retrieves PBX link data for multiple users in a single batch operation. This is a deprecated operation - use BatchGetUsersPbxLinkData instead.

- operationId: `BatchGetUsersPbxLinkDataV1`
- **Request body** (`application/json` — `BatchGetUsersPbxLinkDataV1RequestContent`) **(required)**
  - `id` — array **(required)** _(minItems=1; maxItems=500)_
    - _array of_ `string`
- **Response 200** (`BatchGetUsersPbxLinkDataV1ResponseContent`)
  - `users` — array **(required)**
    - _array of_ `UserPbxLinkData`
      - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
      - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
      - `companyName` — string — The name of the tenant (company) associated with the user.
      - `domain` — string **(required)** — The domain of the PBX where the user connected to.
      - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `info` — UserPersonalInfo **(required)**
        - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
        - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
        - `name` — string **(required)** — Name of the user (example: 'John Doe').
        - `extension` — string **(required)** — Extension number of the user (example: '111').
        - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
        - `role` — string **(required)** — Role of the user (example: 'admin').
        - `language` — string **(required)** — Language preference of the user (example: 'en').
        - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
        - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
        - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
        - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
        - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
        - `groupName` — string **(required)** — Name of the user's group.
        - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
        - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
        - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
        - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
        - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
        - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
        - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
      - `pbx` — UserPbxInfo **(required)**
        - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
          - _array of_ `string`
        - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
          - _array of_ `string`
        - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
        - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
        - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
      - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
      - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
      - `port` — string **(required)** — The port used for the PBX connection.
      - `serial` — string **(required)** — The serial number of the PBX.
      - `services` — UserPbxServices
        - `xcaracal` — boolean
        - `wizyWebinar` — boolean
      - `personalSettings` — UserPbxPersonalSettings
      - `dialplanSettings` — UserPbxDialplanSettings
      - `awsRegion` — string — The AWS region where the PBX is located.
      - `updatedAt` — string — The date when link data was updated last time.
- Errors: `400`, `403`, `429`

#### `GET` `/v2/users/GetUserPbxLinkSuggestion`

Retrieves PBX link suggestion information for a user based on their email address. This is a deprecated operation - use GetUserPbxLinkSuggestion instead.

- operationId: `GetUserPbxLinkSuggestionV1`
- **Parameters**
  - `email` (query) — string — An email address of the user when a service token is used. If not provided, the email will be taken from the token. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- **Response 200** (`GetUserPbxLinkSuggestionV1ResponseContent`)
  - `suggestion` — UserPbxLinkSuggestion
    - `domain` — string **(required)** — A domain of the PBX that can be used to connect the user.
    - `port` — string **(required)** — A port of the PBX that can be used to connect the user.
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/UploadPicture`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

Uploads a user profile picture in base64 format and returns the URL where it can be accessed. This is a deprecated operation - use UploadPicture instead.

- operationId: `UploadPictureV1`
- **Request body** (`application/json` — `UploadPictureV1RequestContent`) **(required)**
  - `picture` — string **(required)** — A base64 encoded image file in PNG or JPG format, with dimensions of 140 x 140 pixels.
- **Response 200** (`UploadPictureV1ResponseContent`)
  - `url` — string **(required)**
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/auth/VerifyBotSecretKey`

Verifies a bot secret key and returns bot information if valid. This is a deprecated operation - use VerifyBotSecretKey instead.

- operationId: `VerifyBotSecretKeyV1`
- **Request body** (`application/json` — `VerifyBotSecretKeyV1RequestContent`) **(required)**
  - `secret` — string **(required)** — A secret key string with "sk-" _(minLen=96; maxLen=96)_
- **Response 200** (`VerifyBotSecretKeyV1ResponseContent`)
  - `company` — string **(required)**
  - `id` — string **(required)** — A unique ID for the Bot that corresponds to the bot's x-bees user ID. _(minLen=12; maxLen=12)_
  - `name` — string _(minLen=1; maxLen=64)_
- Errors: `400`, `403`, `429`

### Accounts

#### `GET` `/v2/users/accounts/{accountId}`

Retrieves the account. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `GetAccount`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- **Response 200** (`GetAccountResponseContent`)
  - `account` — Account **(required)**
    - `id` — string **(required)** — Unique identifier of the account. _(minLen=16; maxLen=16)_
    - `defaultWorkspace` — string — The ID of the default workspace, if any. _(minLen=12; maxLen=12)_
    - `primaryIdentity` — string — The identity value (email address or phone number in E.164).
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/users/accounts/{accountId}`

Updates the account. Allows changing default workspace and primary identity. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `UpdateAccount`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- **Request body** (`application/json` — `UpdateAccountRequestContent`)
  - `defaultWorkspace` — string — The workspace to set as default. _(minLen=12; maxLen=12)_
  - `primaryIdentity` — string — The identity value (email or phone) to set as primary.
- **Response 200** (`UpdateAccountResponseContent`)
  - `account` — Account **(required)**
    - `id` — string **(required)** — Unique identifier of the account. _(minLen=16; maxLen=16)_
    - `defaultWorkspace` — string — The ID of the default workspace, if any. _(minLen=12; maxLen=12)_
    - `primaryIdentity` — string — The identity value (email address or phone number in E.164).
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/users/accounts/{accountId}/identities`

Lists all identities (login methods) for the current account. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `ListIdentities`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- **Response 200** (`ListIdentitiesResponseContent`)
  - `identities` — array **(required)**
    - _array of_ `Identity`
      - `identity` — string **(required)** — The identity value (email address or phone number in E.164)
      - `account` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
      - `verified` — boolean — Indicates if the identity is verified.
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/users/accounts/{accountId}/identities`

Adds a new identity (email or phone) to the account. Requires OTP verification for the new identity. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `LinkIdentity`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- **Request body** (`application/json` — `LinkIdentityRequestContent`) **(required)**
  - `identity` — string **(required)** — The identity value: email address or phone number in E.164.
- **Response 200** (`LinkIdentityResponseContent`)
  - `identity` — Identity **(required)**
    - `identity` — string **(required)** — The identity value (email address or phone number in E.164)
    - `account` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
    - `verified` — boolean — Indicates if the identity is verified.
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/users/accounts/{accountId}/identities/verify`

Completes adding an identity by verifying the OTP sent to the new identity. Call after LinkIdentity. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `VerifyIdentity`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- **Request body** (`application/json` — `VerifyIdentityRequestContent`) **(required)**
  - `identity` — string **(required)** — The identity value that was added (email or phone).
  - `otp` — string **(required)** — OTP sent to the new identity to prove ownership.
- **Response 200** (`VerifyIdentityResponseContent`)
  - `identity` — Identity **(required)**
    - `identity` — string **(required)** — The identity value (email address or phone number in E.164)
    - `account` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
    - `verified` — boolean — Indicates if the identity is verified.
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/users/accounts/{accountId}/identities/{identity}`

Removes a non-primary identity from the account. Requires step-up verification for the primary identity. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `UnlinkIdentity`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
  - `identity` (path) — string **(required)** — The identity value (email or phone) to remove.
- Errors: `400`, `403`, `404`, `429`

### Workspaces

#### `GET` `/v2/users/accounts/{accountId}/workspaces`

Lists workspaces available to the account. Without limit, returns every workspace. With limit, returns one page of active work workspaces: query narrows that set by PBX domain before the page is sliced, offset skips into the filtered set, and each workspace includes pbxUser when a PBX record exists. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `ListWorkspaces`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
  - `limit` (query) — number — Maximum number of selectable workspaces to return, from 1 to 100. When omitted, every workspace is returned and offset and query are ignored. _(min=1; max=100)_
  - `offset` (query) — number — Number of selectable workspaces to skip before this page. Applied only when limit is set. Defaults to 0. An offset past the end returns an empty page. _(min=0)_
  - `query` (query) — string — Case-insensitive substring matched against the PBX domain. Applied only when limit is set. Blank values are ignored. Narrows total as well as the page.
- **Response 200** (`ListWorkspacesResponseContent`)
  - `workspaces` — array **(required)** — Workspaces for this request. A paged response contains only active work workspaces, ordered with the account default first, then workspaces the user linked to before (most recent first), then the rest by domain.
    - _array of_ `Workspace`
      - `companyId` — string — The unique identifier of the tenant (company). _(minLen=3; maxLen=30)_
      - `pbxUser` — UserPbxLinkData
        - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
        - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
        - `companyName` — string — The name of the tenant (company) associated with the user.
        - `domain` — string **(required)** — The domain of the PBX where the user connected to.
        - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
        - `info` — UserPersonalInfo **(required)**
          - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
          - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
          - `name` — string **(required)** — Name of the user (example: 'John Doe').
          - `extension` — string **(required)** — Extension number of the user (example: '111').
          - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
          - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
          - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
          - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
          - `role` — string **(required)** — Role of the user (example: 'admin').
          - `language` — string **(required)** — Language preference of the user (example: 'en').
          - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
          - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
          - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
          - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
          - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
          - `groupName` — string **(required)** — Name of the user's group.
          - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
          - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
          - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
          - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
          - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
          - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
          - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
        - `pbx` — UserPbxInfo **(required)**
          - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
            - _array of_ `string`
          - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
            - _array of_ `string`
          - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
          - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
          - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
        - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
        - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
        - `port` — string **(required)** — The port used for the PBX connection.
        - `serial` — string **(required)** — The serial number of the PBX.
        - `services` — UserPbxServices
          - `xcaracal` — boolean
          - `wizyWebinar` — boolean
        - `personalSettings` — UserPbxPersonalSettings
        - `dialplanSettings` — UserPbxDialplanSettings
        - `awsRegion` — string — The AWS region where the PBX is located.
        - `updatedAt` — string — The date when link data was updated last time.
      - `streamUser` — User
        - `id` — string **(required)** _(minLen=12; maxLen=12)_
        - `name` — string
        - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
        - `phone` — string
        - `picture` — string
        - `locale` — string
        - `timeZone` — string
        - `company` — string
        - `bot` — boolean
        - `pbxDomain` — string
        - `pbxPort` — string
        - `pbxExtension` — string
        - `pbxSerial` — string
        - `pbxUserId` — string
        - `pbxGroupId` — string
        - `createdAt` — string
        - `updatedAt` — string
      - `type` — string _(enum: `personal`, `work`, `support`)_
      - `id` — string **(required)** — The unique identifier _(minLen=12; maxLen=12)_
      - `accountId` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
      - `active` — boolean **(required)** — Indicates if the workspace is active.
  - `total` — number — Number of selectable workspaces (active and type work) that match query, ignoring offset. Present when limit is set.
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/users/accounts/{accountId}/workspaces/{workspaceId}`

Updates the workspace. Available only via s2s (service-to-service) authentication.

- operationId: `UpdateWorkspace`
- **Parameters**
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
  - `workspaceId` (path) — string **(required)** — The unique identifier of the workspace to deactivate. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UpdateWorkspaceRequestContent`)
  - `active` — boolean — Indicates if the workspace is active.
  - `type` — string _(enum: `personal`, `work`, `support`)_
- **Response 200** (`UpdateWorkspaceResponseContent`)
  - `workspace` — Workspace **(required)**
    - `companyId` — string — The unique identifier of the tenant (company). _(minLen=3; maxLen=30)_
    - `pbxUser` — UserPbxLinkData
      - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
      - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
      - `companyName` — string — The name of the tenant (company) associated with the user.
      - `domain` — string **(required)** — The domain of the PBX where the user connected to.
      - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `info` — UserPersonalInfo **(required)**
        - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
        - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
        - `name` — string **(required)** — Name of the user (example: 'John Doe').
        - `extension` — string **(required)** — Extension number of the user (example: '111').
        - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
        - `role` — string **(required)** — Role of the user (example: 'admin').
        - `language` — string **(required)** — Language preference of the user (example: 'en').
        - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
        - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
        - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
        - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
        - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
        - `groupName` — string **(required)** — Name of the user's group.
        - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
        - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
        - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
        - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
        - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
        - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
        - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
      - `pbx` — UserPbxInfo **(required)**
        - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
          - _array of_ `string`
        - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
          - _array of_ `string`
        - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
        - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
        - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
      - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
      - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
      - `port` — string **(required)** — The port used for the PBX connection.
      - `serial` — string **(required)** — The serial number of the PBX.
      - `services` — UserPbxServices
        - `xcaracal` — boolean
        - `wizyWebinar` — boolean
      - `personalSettings` — UserPbxPersonalSettings
      - `dialplanSettings` — UserPbxDialplanSettings
      - `awsRegion` — string — The AWS region where the PBX is located.
      - `updatedAt` — string — The date when link data was updated last time.
    - `streamUser` — User
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
    - `type` — string _(enum: `personal`, `work`, `support`)_
    - `id` — string **(required)** — The unique identifier _(minLen=12; maxLen=12)_
    - `accountId` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
    - `active` — boolean **(required)** — Indicates if the workspace is active.
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/users/accounts/{accountId}/workspaces/{workspaceId}`

Removes the connection between the account and a workspace. Available via s2s (service-to-service) or the x-bees token of the account owner; API keys are refused.

- operationId: `UnlinkWorkspace`
- **Parameters**
  - `workspaceId` (path) — string **(required)** — The unique identifier of the workspace (Stream user ID). _(minLen=12; maxLen=12)_
  - `accountId` (path) — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- Errors: `400`, `403`, `404`, `429`

### Users

#### `GET` `/v2/users/app-version`

Returns the current Google Play Store version of the Android app for the specified appType (X-Bees, X-Hoppers, Collaboration).

- operationId: `GetAppVersion`
- **Scopes**: `users:GetAppVersion`, `users:read`
- **Parameters**
  - `appType` (query) — string **(required)** _(enum: `x-bees`, `x-hoppers`, `collaboration`)_
- **Response 200** (`GetAppVersionResponseContent`)
  - `version` — string **(required)** _(pattern=^[0-9]+\.[0-9]+\.[0-9]+$)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/batch-get-users`

Retrieves details of multiple users in a single batch operation.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 60 |
| XBS | 3600 | 600 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 600 |

- operationId: `BatchGetUsers`
- **Scopes**: `users:BatchGetUsers`, `users:read`
- **Request body** (`application/json` — `BatchGetUsersRequestContent`) **(required)**
  - `id` — array **(required)** _(minItems=1; maxItems=500)_
    - _array of_ `string`
- **Response 200** (`BatchGetUsersResponseContent`)
  - `users` — array **(required)** — A list of users that exist in the platform.
    - _array of_ `User`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/batch-get-users-pbx-link-data`

Retrieves PBX link data for multiple users in a single batch operation.

- operationId: `BatchGetUsersPbxLinkData`
- **Scopes**: `users:BatchGetUsersPbxLinkData`, `users:read`
- **Request body** (`application/json` — `BatchGetUsersPbxLinkDataRequestContent`) **(required)**
  - `id` — array **(required)** _(minItems=1; maxItems=500)_
    - _array of_ `string`
- **Response 200** (`BatchGetUsersPbxLinkDataResponseContent`)
  - `users` — array **(required)**
    - _array of_ `UserPbxLinkData`
      - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
      - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
      - `companyName` — string — The name of the tenant (company) associated with the user.
      - `domain` — string **(required)** — The domain of the PBX where the user connected to.
      - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `info` — UserPersonalInfo **(required)**
        - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
        - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
        - `name` — string **(required)** — Name of the user (example: 'John Doe').
        - `extension` — string **(required)** — Extension number of the user (example: '111').
        - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
        - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
        - `role` — string **(required)** — Role of the user (example: 'admin').
        - `language` — string **(required)** — Language preference of the user (example: 'en').
        - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
        - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
        - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
        - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
        - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
        - `groupName` — string **(required)** — Name of the user's group.
        - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
        - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
        - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
        - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
        - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
        - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
        - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
      - `pbx` — UserPbxInfo **(required)**
        - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
          - _array of_ `string`
        - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
          - _array of_ `string`
        - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
        - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
        - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
      - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
      - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
      - `port` — string **(required)** — The port used for the PBX connection.
      - `serial` — string **(required)** — The serial number of the PBX.
      - `services` — UserPbxServices
        - `xcaracal` — boolean
        - `wizyWebinar` — boolean
      - `personalSettings` — UserPbxPersonalSettings
      - `dialplanSettings` — UserPbxDialplanSettings
      - `awsRegion` — string — The AWS region where the PBX is located.
      - `updatedAt` — string — The date when link data was updated last time.
- Errors: `400`, `403`, `429`

#### `GET` `/v2/users/cloud/{userId}`

Retrieves details of a specific user by their unique identifier.

- operationId: `GetUser`
- **Scopes**: `users:GetUser`, `users:read`
- **Parameters**
  - `userId` (path) — string **(required)** — The unique identifier of the user. _(minLen=12; maxLen=12)_
- **Response 200** (`GetUserResponseContent`)
  - `user` — User **(required)**
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/users/cloud/{userId}/pbx-link-data`

Retrieves PBX link data for a specific user.

- operationId: `GetUserPbxLinkData`
- **Scopes**: `users:GetUserPbxLinkData`, `users:read`
- **Parameters**
  - `userId` (path) — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
- **Response 200** (`GetUserPbxLinkDataResponseContent`)
  - `user` — UserPbxLinkData **(required)**
    - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
    - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
    - `companyName` — string — The name of the tenant (company) associated with the user.
    - `domain` — string **(required)** — The domain of the PBX where the user connected to.
    - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `info` — UserPersonalInfo **(required)**
      - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
      - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
      - `name` — string **(required)** — Name of the user (example: 'John Doe').
      - `extension` — string **(required)** — Extension number of the user (example: '111').
      - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
      - `role` — string **(required)** — Role of the user (example: 'admin').
      - `language` — string **(required)** — Language preference of the user (example: 'en').
      - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
      - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
      - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
      - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
      - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
      - `groupName` — string **(required)** — Name of the user's group.
      - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
      - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
      - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
      - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
      - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
      - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
      - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
    - `pbx` — UserPbxInfo **(required)**
      - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
        - _array of_ `string`
      - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
        - _array of_ `string`
      - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
      - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
      - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
    - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
    - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
    - `port` — string **(required)** — The port used for the PBX connection.
    - `serial` — string **(required)** — The serial number of the PBX.
    - `services` — UserPbxServices
      - `xcaracal` — boolean
      - `wizyWebinar` — boolean
    - `personalSettings` — UserPbxPersonalSettings
    - `dialplanSettings` — UserPbxDialplanSettings
    - `awsRegion` — string — The AWS region where the PBX is located.
    - `updatedAt` — string — The date when link data was updated last time.
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/users/get-user-pbx-link-suggestion`

Retrieves PBX link suggestion information for a user based on their email address.

- operationId: `GetUserPbxLinkSuggestion`
- **Scopes**: `users:GetUserPbxLinkSuggestion`, `users:read`
- **Parameters**
  - `email` (query) — string — An email address of the user when a service token is used. If not provided, the email will be taken from the token. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- **Response 200** (`GetUserPbxLinkSuggestionResponseContent`)
  - `suggestion` — UserPbxLinkSuggestion
    - `domain` — string **(required)** — A domain of the PBX that can be used to connect the user.
    - `port` — string **(required)** — A port of the PBX that can be used to connect the user.
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/query-colleagues`

Searches for colleagues using various filters and search criteria, with optional auto-invitation for new users.

- operationId: `QueryColleagues`
- **Scopes**: `users:QueryColleagues`, `users:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `QueryColleaguesRequestContent`)
  - `query` — QueryColleaguesParameters
    - `id` — array
      - _array of_ `string`
    - `extension` — array
      - _array of_ `string`
    - `officePhone` — array
      - _array of_ `string`
    - `mobilePhone` — array
      - _array of_ `string`
    - `name` — array
      - _array of_ `string`
    - `email` — array
      - _array of_ `string`
    - `department` — array
      - _array of_ `string`
    - `search` — string
    - `searchFields` — array
      - _array of_ `PbxColleaguesQueryField`
    - `searchStrategy` — string _(enum: `contain`, `startsWith`)_
    - `sort` — array
      - _array of_ `PbxColleaguesQueryField`
    - `start` — number
    - `count` — number _(default=50; min=1; max=50)_
    - `dir` — string _(enum: `asc`, `desc`)_
  - `invite` — boolean — If enabled, the system will automatically invite users for colleagues returned from the PBX if they haven't logged in yet.
- **Response 200** (`QueryColleaguesResponseContent`)
  - `colleagues` — array **(required)** — A list of users that exist in the platform and matches predicate if specified.
    - _array of_ `QueryColleaguesOutputItem`
      - `user` — User
        - `id` — string **(required)** _(minLen=12; maxLen=12)_
        - `name` — string
        - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
        - `phone` — string
        - `picture` — string
        - `locale` — string
        - `timeZone` — string
        - `company` — string
        - `bot` — boolean
        - `pbxDomain` — string
        - `pbxPort` — string
        - `pbxExtension` — string
        - `pbxSerial` — string
        - `pbxUserId` — string
        - `pbxGroupId` — string
        - `createdAt` — string
        - `updatedAt` — string
      - `colleague` — PbxColleague **(required)**
        - `id` — string **(required)**
        - `name` — string
        - `login` — string
        - `extension` — string **(required)**
        - `officePhone` — string
        - `mobilePhone` — string
        - `faxNumber` — string
        - `email` — string
        - `pbxDn` — string **(required)**
        - `pbx` — string **(required)**
        - `role` — string **(required)** _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
        - `groupName` — string **(required)**
        - `groupDn` — string **(required)**
        - `language` — string **(required)**
        - `dialplan` — string **(required)**
        - `faxDialplan` — string **(required)**
        - `department` — string
        - `picture` — string **(required)**
        - `sourceId` — string
        - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
        - `jid` — string **(required)**
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/query-user`

Searches for a single user using a query with optional predicate validation.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 30 |
| XBS | 3600 | 200 |
| XBS_BOT | 60 | 30 |
| XBS_BOT | 3600 | 200 |

- operationId: `QueryUser`
- **Scopes**: `users:QueryUser`, `users:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. A user who has a workspace in this tenant is returned as that workspace instead of the default one. Other tokens use the tenant they were issued for. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `QueryUserRequestContent`) **(required)**
  - `query` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`id`**
        - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX).
      - **`email`**
        - `email` — string **(required)** — The email address of the user.
      - **`phone`**
        - `phone` — string **(required)** — The phone number of the user.
  - `predicate` — UserQueryPredicate
    - `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- **Response 200** (`QueryUserResponseContent`)
  - `user` — User **(required)**
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/users/query-users`

Searches for multiple users using queries with optional predicate validation.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 2 |
| XBS | 3600 | 8 |
| XBS_BOT | 60 | 2 |
| XBS_BOT | 3600 | 8 |

- operationId: `QueryUsers`
- **Scopes**: `users:QueryUsers`, `users:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. A user who has a workspace in this tenant is returned as that workspace instead of the default one. Other tokens use the tenant they were issued for. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `QueryUsersRequestContent`) **(required)**
  - `queries` — array **(required)** _(minItems=1; maxItems=50)_
    - _array of_ `UserQuery`
      - _oneOf_ — exactly one of:
        - **`id`**
          - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX).
        - **`email`**
          - `email` — string **(required)** — The email address of the user.
        - **`phone`**
          - `phone` — string **(required)** — The phone number of the user.
  - `predicate` — UserQueryPredicate
    - `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- **Response 200** (`QueryUsersResponseContent`)
  - `users` — array **(required)** — A list of users that exist in the platform and matches predicate if specified.
    - _array of_ `User`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
- Errors: `400`, `403`, `429`

### Other

#### `POST` `/v2/users/batch-get-users-email-notifications-settings`

Get multiple user settings by their IDs

- operationId: `BatchGetUsersEmailNotificationsSettings`
- **Scopes**: `users:BatchGetUsersEmailNotificationsSettings`, `users:read`
- **Request body** (`application/json` — `BatchGetUsersEmailNotificationsSettingsRequestContent`) **(required)**
  - `usersIds` — array **(required)** — The users to read, 1 to 500 ids. A PBX token or an API key gets the stored settings only of the users of its own company; any other id gets the default settings, as an unknown id does. _(minItems=1; maxItems=500)_
    - _array of_ `string`
- **Response 200** (`BatchGetUsersEmailNotificationsSettingsResponseContent`)
  - `notifications` — UsersEmailNotificationsSettingsMap **(required)**
    - _map of_ `UserEmailNotificationsSettings`
      - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
      - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.
- Errors: `400`, `403`, `429`

#### `GET` `/v2/users/bots/{botId}`

Retrieves details of a specific bot by its unique identifier.

- operationId: `GetBot`
- **Scopes**: `users:GetBot`, `users:read`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Response 200** (`GetBotResponseContent`)
  - `bot` — Bot **(required)**
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `picture` — string — A link to the bot picture.
    - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
    - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
    - `integrationApiKeysCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `updated` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/users/bots/{botId}/callback`

Retrieves the callback configuration for a specific bot.

- operationId: `GetBotCallback`
- **Scopes**: `users:GetBotCallback`, `users:read`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Response 200** (`GetBotCallbackResponseContent`)
  - `callback` — BotCallback **(required)**
    - `endpoint` — union
      - _oneOf_ — exactly one of:
        - **`llm`**
          - `llm` — BotLlmEndpoint **(required)**
            - `prompt` — string **(required)** _(maxLen=40000)_
            - `guidelines` — array
              - _array of_ `string`
            - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `embeddedTools` — array — Embedded functions to use within chat session.
              - _array of_ `BotLlmEmbeddedTool`
                - _(nesting depth limit — see `BotLlmEmbeddedTool` in the Schemas appendix)_
            - `tools` — array — Custom tools to be used within chat session.
              - _array of_ `BotLlmTool`
                - _(nesting depth limit — see `BotLlmTool` in the Schemas appendix)_
            - `capabilities` — array
              - _array of_ `BotCapability`
                - _(nesting depth limit — see `BotCapability` in the Schemas appendix)_
        - **`dialogflowCx`**
          - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
            - `credentials` — any **(required)** — Dialogflow Service Account Credentials
            - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
            - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
            - `language` — string **(required)** — Language
        - **`openAiAssistant`**
          - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
            - `key` — string **(required)**
            - `assistantId` — string **(required)**
        - **`webhook`**
          - `webhook` — BotWebhookEndpoint **(required)**
            - `url` — string **(required)**
            - `secret` — string **(required)**
        - **`sqs`**
          - `sqs` — BotSqsEndpoint **(required)**
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — string **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/users/bots/{botId}/callback`

Updates the callback configuration for a specific bot.

- operationId: `UpdateBotCallback`
- **Scopes**: `users:UpdateBotCallback`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Request body** (`application/json` — `UpdateBotCallbackRequestContent`) **(required)**
  - `callback` — BotCallback **(required)**
    - `endpoint` — union
      - _oneOf_ — exactly one of:
        - **`llm`**
          - `llm` — BotLlmEndpoint **(required)**
            - `prompt` — string **(required)** _(maxLen=40000)_
            - `guidelines` — array
              - _array of_ `string`
            - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `embeddedTools` — array — Embedded functions to use within chat session.
              - _array of_ `BotLlmEmbeddedTool`
                - _(nesting depth limit — see `BotLlmEmbeddedTool` in the Schemas appendix)_
            - `tools` — array — Custom tools to be used within chat session.
              - _array of_ `BotLlmTool`
                - _(nesting depth limit — see `BotLlmTool` in the Schemas appendix)_
            - `capabilities` — array
              - _array of_ `BotCapability`
                - _(nesting depth limit — see `BotCapability` in the Schemas appendix)_
        - **`dialogflowCx`**
          - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
            - `credentials` — any **(required)** — Dialogflow Service Account Credentials
            - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
            - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
            - `language` — string **(required)** — Language
        - **`openAiAssistant`**
          - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
            - `key` — string **(required)**
            - `assistantId` — string **(required)**
        - **`webhook`**
          - `webhook` — BotWebhookEndpoint **(required)**
            - `url` — string **(required)**
            - `secret` — string **(required)**
        - **`sqs`**
          - `sqs` — BotSqsEndpoint **(required)**
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — string **(required)**
- **Response 200** (`UpdateBotCallbackResponseContent`)
  - `callback` — BotCallback **(required)**
    - `endpoint` — union
      - _oneOf_ — exactly one of:
        - **`llm`**
          - `llm` — BotLlmEndpoint **(required)**
            - `prompt` — string **(required)** _(maxLen=40000)_
            - `guidelines` — array
              - _array of_ `string`
            - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `embeddedTools` — array — Embedded functions to use within chat session.
              - _array of_ `BotLlmEmbeddedTool`
                - _(nesting depth limit — see `BotLlmEmbeddedTool` in the Schemas appendix)_
            - `tools` — array — Custom tools to be used within chat session.
              - _array of_ `BotLlmTool`
                - _(nesting depth limit — see `BotLlmTool` in the Schemas appendix)_
            - `capabilities` — array
              - _array of_ `BotCapability`
                - _(nesting depth limit — see `BotCapability` in the Schemas appendix)_
        - **`dialogflowCx`**
          - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
            - `credentials` — any **(required)** — Dialogflow Service Account Credentials
            - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
            - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
            - `language` — string **(required)** — Language
        - **`openAiAssistant`**
          - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
            - `key` — string **(required)**
            - `assistantId` — string **(required)**
        - **`webhook`**
          - `webhook` — BotWebhookEndpoint **(required)**
            - `url` — string **(required)**
            - `secret` — string **(required)**
        - **`sqs`**
          - `sqs` — BotSqsEndpoint **(required)**
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — string **(required)**
- Errors: `400`, `403`, `429`

#### `PUT` `/v2/users/change-email`

Schedules user's email changing.

- operationId: `ChangeUserEmail`
- **Scopes**: `users:ChangeUserEmail`
- **Request body** (`application/json` — `ChangeUserEmailRequestContent`) **(required)**
  - `newData` — NewEmailData **(required)**
    - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `companyId` — string — By default, API expects that company id will be the same for both new and old emails. If no - this field should be provided _(minLen=3; maxLen=30)_
    - `pbxDomain` — string — Target PBX domain name for cases with few PBXes in one WMS-network
  - `oldData` — OldEmailData **(required)**
    - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `companyId` — string — By default, API expects that company id will be the same for both new and old emails. If no - this field should be provided _(minLen=3; maxLen=30)_
- **Response 200** (`ChangeUserEmailResponseContent`)
  - `sfnArn` — string **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/users/cloud/{userId}/notifications/email`

Getting user email notifications settings

- operationId: `GetUserEmailNotificationsSettings`
- **Scopes**: `users:GetUserEmailNotificationsSettings`, `users:read`
- **Parameters**
  - `userId` (path) — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
- **Response 200** (`GetUserEmailNotificationsSettingsResponseContent`)
  - `notifications` — UserEmailNotificationsSettings **(required)**
    - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
    - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/users/cloud/{userId}/notifications/email`

Update user email notifications settings

- operationId: `UpdateUserEmailNotificationsSettings`
- **Scopes**: `users:UpdateUserEmailNotificationsSettings`
- **Parameters**
  - `userId` (path) — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UpdateUserEmailNotificationsSettingsRequestContent`)
  - `unread` — boolean — A flag that indicates whether the system should send email notifications about unread messages.
  - `transcription` — boolean — A flag that indicates whether the system should send email notifications about AI transcription.
- **Response 200** (`UpdateUserEmailNotificationsSettingsResponseContent`)
  - `notifications` — UserEmailNotificationsSettings **(required)**
    - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
    - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.
- Errors: `400`, `403`, `429`

#### `PATCH` `/v2/users/cloud/{userId}/notifications/email`

Partially update user email notifications settings

- operationId: `PartialUpdateUserEmailNotificationsSettings`
- **Scopes**: `users:PartialUpdateUserEmailNotificationsSettings`
- **Parameters**
  - `userId` (path) — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `PartialUpdateUserEmailNotificationsSettingsRequestContent`)
  - `unread` — boolean — A flag that indicates whether the system should send email notifications about unread messages.
  - `transcription` — boolean — A flag that indicates whether the system should send email notifications about AI transcription.
- **Response 200** (`PartialUpdateUserEmailNotificationsSettingsResponseContent`)
  - `notifications` — UserEmailNotificationsSettings **(required)**
    - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
    - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/create-anonymous-session`

- operationId: `CreateAnonymousSession`
- **Request body** (`application/json` — `CreateAnonymousSessionRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=1; maxLen=50)_
  - `captchaProof` — string **(required)** _(maxLen=4096)_
  - `context` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`widgetId`**
        - `widgetId` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
      - **`channelId`**
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- **Response 200** (`CreateAnonymousSessionResponseContent`)
  - `syntheticEmail` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/users/intelligence-search`

Search user in the directory using AI. Result is sorted by relevance.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| PBX | 10 | 30 |
| PBX | 3600 | 600 |

- operationId: `IntelligenceSearch`
- **Scopes**: `users:IntelligenceSearch`, `users:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. Only for s2s auth _(minLen=3; maxLen=30)_
  - `search` (query) — string **(required)**
  - `excludeExtension` (query) — string — Optional extension to exclude from search results. Used to prevent returning the caller's own record when searching. _(minLen=2; maxLen=50)_
- **Response 200** (`IntelligenceSearchResponseContent`)
  - `items` — array **(required)**
    - _array of_ `DirectoryItem`
      - `extension` — string **(required)**
      - `name` — string **(required)**
      - `department` — string
      - `group` — string
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/toggle-transcription-email-notifications-subscription`

Using unsubscribeToken from email you can Toggle transcription email notifications subscription

- operationId: `ToggleTranscriptionEmailNotificationsSubscription`
- **Scopes**: `users:ToggleTranscriptionEmailNotificationsSubscription`
- **Request body** (`application/json` — `ToggleTranscriptionEmailNotificationsSubscriptionRequestContent`) **(required)**
  - `unsubscribeToken` — string **(required)**
  - `subscribe` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/toggle-unread-email-notifications-subscription`

Using unsubscribeToken from email you can Toggle unread messages email notifications subscription

- operationId: `ToggleUnreadEmailNotificationsSubscription`
- **Scopes**: `users:ToggleUnreadEmailNotificationsSubscription`
- **Request body** (`application/json` — `ToggleUnreadEmailNotificationsSubscriptionRequestContent`) **(required)**
  - `unsubscribeToken` — string **(required)**
  - `subscribe` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
- Errors: `400`, `403`, `429`

### Bots

#### `GET` `/v2/users/bots`

Retrieves a list of all bots for the specified company.

- operationId: `ListBots`
- **Scopes**: `users:ListBots`, `users:read`
- **Parameters**
  - `company` (query) — string
- **Response 200** (`ListBotsResponseContent`)
  - `bots` — array **(required)**
    - _array of_ `Bot`
      - `name` — string **(required)** _(minLen=3; maxLen=255)_
      - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
      - `picture` — string — A link to the bot picture.
      - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
      - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
      - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
      - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
      - `integrationApiKeysCount` — number **(required)**
      - `createdAt` — string **(required)**
      - `updated` — string
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/bots`

Creates a new bot with the specified configuration and callback settings.

- operationId: `CreateBot`
- **Scopes**: `users:CreateBot`
- **Parameters**
  - `company` (query) — string
- **Request body** (`application/json` — `CreateBotRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `picture` — string — A link to the bot picture.
  - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
  - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
  - `id` — string — Optional bot id. Omit to mint a random 12-character id. Supply a Wilma agent id (`a_` plus 10) so RNA search and conversation members share that id. Conflicts if the id already exists. _(minLen=12; maxLen=12)_
  - `callback` — BotCallback **(required)**
    - `endpoint` — union
      - _oneOf_ — exactly one of:
        - **`llm`**
          - `llm` — BotLlmEndpoint **(required)**
            - `prompt` — string **(required)** _(maxLen=40000)_
            - `guidelines` — array
              - _array of_ `string`
            - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
            - `embeddedTools` — array — Embedded functions to use within chat session.
              - _array of_ `BotLlmEmbeddedTool`
                - _(nesting depth limit — see `BotLlmEmbeddedTool` in the Schemas appendix)_
            - `tools` — array — Custom tools to be used within chat session.
              - _array of_ `BotLlmTool`
                - _(nesting depth limit — see `BotLlmTool` in the Schemas appendix)_
            - `capabilities` — array
              - _array of_ `BotCapability`
                - _(nesting depth limit — see `BotCapability` in the Schemas appendix)_
        - **`dialogflowCx`**
          - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
            - `credentials` — any **(required)** — Dialogflow Service Account Credentials
            - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
            - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
            - `language` — string **(required)** — Language
        - **`openAiAssistant`**
          - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
            - `key` — string **(required)**
            - `assistantId` — string **(required)**
        - **`webhook`**
          - `webhook` — BotWebhookEndpoint **(required)**
            - `url` — string **(required)**
            - `secret` — string **(required)**
        - **`sqs`**
          - `sqs` — BotSqsEndpoint **(required)**
            - `url` — string **(required)**
            - `key` — string **(required)**
            - `secret` — string **(required)**
- **Response 200** (`CreateBotResponseContent`)
  - `bot` — Bot **(required)**
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `picture` — string — A link to the bot picture.
    - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
    - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
    - `integrationApiKeysCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `updated` — string
- Errors: `400`, `403`, `409`, `429`

#### `PUT` `/v2/users/bots/{botId}`

Updates the configuration of an existing bot.

- operationId: `UpdateBot`
- **Scopes**: `users:UpdateBot`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Request body** (`application/json` — `UpdateBotRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `picture` — string — A link to the bot picture.
  - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
  - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
- **Response 200** (`UpdateBotResponseContent`)
  - `bot` — Bot **(required)**
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `picture` — string — A link to the bot picture.
    - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
    - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
    - `integrationApiKeysCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `updated` — string
- Errors: `400`, `403`, `429`

#### `DELETE` `/v2/users/bots/{botId}`

Deletes an existing bot and all its associated data.

- operationId: `DeleteBot`
- **Scopes**: `users:DeleteBot`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/users/bots/{botId}/keys`

Retrieves a list of API keys associated with a specific bot.

- operationId: `ListBotApiKeys`
- **Scopes**: `users:ListBotApiKeys`, `users:read`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Response 200** (`ListBotApiKeysResponseContent`)
  - `keys` — array **(required)**
    - _array of_ `BotApiKey`
      - `secret` — string **(required)** _(minLen=96; maxLen=96)_
      - `name` — string _(minLen=1; maxLen=64)_
      - `createdAt` — string **(required)**
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/bots/{botId}/keys`

Creates a new API key for a specific bot.

- operationId: `CreateBotApiKey`
- **Scopes**: `users:CreateBotApiKey`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `company` (query) — string
- **Request body** (`application/json` — `CreateBotApiKeyRequestContent`)
  - `name` — string _(minLen=1; maxLen=64)_
- **Response 200** (`CreateBotApiKeyResponseContent`)
  - `bot` — Bot **(required)**
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `picture` — string — A link to the bot picture.
    - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
    - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
    - `integrationApiKeysCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `updated` — string
  - `key` — BotApiKey **(required)**
    - `secret` — string **(required)** _(minLen=96; maxLen=96)_
    - `name` — string _(minLen=1; maxLen=64)_
    - `createdAt` — string **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/users/bots/{botId}/keys/{apiKeySecret}`

Deletes an existing API key for a specific bot.

- operationId: `DeleteBotApiKey`
- **Scopes**: `users:DeleteBotApiKey`
- **Parameters**
  - `botId` (path) — string **(required)** _(minLen=12; maxLen=12)_
  - `apiKeySecret` (path) — string **(required)** _(minLen=96; maxLen=96)_
  - `company` (query) — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/users/system-bots`

Creates a new system bot with basic configuration for internal use.

- operationId: `CreateSystemBot`
- **Scopes**: `users:CreateSystemBot`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateSystemBotRequestContent`) **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `picture` — string — A URL pointing to the bot's avatar.
- **Response 200** (`CreateSystemBotResponseContent`)
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `429`

### Members

#### `POST` `/v2/users/invite`

Invite a list of users to x-bees. This operation creates an account for specified emails or phone numbers. Use this method to create users who can be added to conversations later.
If an invitee resolves to an account that is currently deactivated in GetStream, the operation does not fail; instead, that invitee is reported in `skippedInvitees` and is not included in `users`.


**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 15 |
| XBS | 3600 | 30 |
| XBS_BOT | 60 | 50 |
| XBS_BOT | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |

- operationId: `Invite`
- **Scopes**: `users:Invite`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `InviteRequestContent`) **(required)**
  - `invitees` — array **(required)** — A list of users to invite. The list must contain between 1 and 20 users. _(minItems=1; maxItems=20)_
    - _array of_ `UserToInvite`
      - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
      - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
      - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
- **Response 200** (`InviteResponseContent`)
  - `users` — array **(required)** — A list of users who were successfully invited. Each entry contains only id, name, email, phone, picture, company, pbxUserId, and locale.
    - _array of_ `InvitedUser`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string — Avatar URL. Notification emails render it as the sender's avatar.
      - `company` — string — Tenant id. Callers use it to tell a colleague from an external user.
      - `pbxUserId` — string — PBX user id of a colleague. A caller that already knows the colleague matches the invite result by this value.
      - `locale` — string — Preferred user language. Notification emails sent to the invitee use it to pick the template language.
  - `skippedInvitees` — array **(required)** — A list of invitees that were skipped during the operation, for example because the resolved account is deactivated in GetStream. Each entry carries the email or phone supplied in the request, and the user id when it was already known.
    - _array of_ `SkippedMember`
      - `id` — string — The unique identifier of the skipped user if it is known. _(minLen=12; maxLen=12)_
      - `email` — string — The email address of the skipped user if it is known. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string — The phone number of the skipped user if it is known. _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- Errors: `400`, `403`, `429`

### Utils

#### `POST` `/v2/users/upload-picture`

Uploads a user profile picture in base64 format and returns the URL where it can be accessed.

- operationId: `UploadPicture`
- **Scopes**: `messaging:UploadPicture`, `users:UploadPicture`
- **Request body** (`application/json` — `UploadPictureRequestContent`) **(required)**
  - `picture` — string **(required)** — A base64 encoded image file in PNG or JPG format, with dimensions of 140 x 140 pixels.
- **Response 200** (`UploadPictureResponseContent`)
  - `url` — string **(required)**
- Errors: `400`, `403`, `429`

#### `POST` `/v2/users/verify-bot-secret-key`

Verifies a bot secret key and returns bot information if valid.

- operationId: `VerifyBotSecretKey`
- **Scopes**: `users:VerifyBotSecretKey`
- **Request body** (`application/json` — `VerifyBotSecretKeyRequestContent`) **(required)**
  - `secret` — string **(required)** — A secret key string with "sk-" _(minLen=96; maxLen=96)_
- **Response 200** (`VerifyBotSecretKeyResponseContent`)
  - `company` — string **(required)**
  - `id` — string **(required)** — A unique ID for the Bot that corresponds to the bot's x-bees user ID. _(minLen=12; maxLen=12)_
  - `name` — string _(minLen=1; maxLen=64)_
- Errors: `400`, `403`, `429`

### Schemas appendix — Users & ChatBots API

<details><summary>150 component schemas</summary>

**`Account`**

- `id` — string **(required)** — Unique identifier of the account. _(minLen=16; maxLen=16)_
- `defaultWorkspace` — string — The ID of the default workspace, if any. _(minLen=12; maxLen=12)_
- `primaryIdentity` — string — The identity value (email address or phone number in E.164).

**`AccountNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`AnonymousEntryContext`**

- _oneOf_ — exactly one of:
  - **`widgetId`**
    - `widgetId` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
  - **`channelId`**
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`AppType`**

- string _(enum: `x-bees`, `x-hoppers`, `collaboration`)_

**`BatchGetUsersEmailNotificationsSettingsRequestContent`**

- `usersIds` — array **(required)** — The users to read, 1 to 500 ids. A PBX token or an API key gets the stored settings only of the users of its own company; any other id gets the default settings, as an unknown id does. _(minItems=1; maxItems=500)_
  - _array of_ `string`

**`BatchGetUsersEmailNotificationsSettingsResponseContent`**

- `notifications` — UsersEmailNotificationsSettingsMap **(required)**
  - _map of_ `UserEmailNotificationsSettings`
    - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
    - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.

**`BatchGetUsersPbxLinkDataRequestContent`**

- `id` — array **(required)** _(minItems=1; maxItems=500)_
  - _array of_ `string`

**`BatchGetUsersPbxLinkDataResponseContent`**

- `users` — array **(required)**
  - _array of_ `UserPbxLinkData`
    - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
    - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
    - `companyName` — string — The name of the tenant (company) associated with the user.
    - `domain` — string **(required)** — The domain of the PBX where the user connected to.
    - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `info` — UserPersonalInfo **(required)**
      - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
      - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
      - `name` — string **(required)** — Name of the user (example: 'John Doe').
      - `extension` — string **(required)** — Extension number of the user (example: '111').
      - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
      - `role` — string **(required)** — Role of the user (example: 'admin').
      - `language` — string **(required)** — Language preference of the user (example: 'en').
      - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
      - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
      - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
      - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
      - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
      - `groupName` — string **(required)** — Name of the user's group.
      - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
      - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
      - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
      - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
      - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
      - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
      - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
    - `pbx` — UserPbxInfo **(required)**
      - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
        - _array of_ `string`
      - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
        - _array of_ `string`
      - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
      - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
      - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
    - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
    - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
    - `port` — string **(required)** — The port used for the PBX connection.
    - `serial` — string **(required)** — The serial number of the PBX.
    - `services` — UserPbxServices
      - `xcaracal` — boolean
      - `wizyWebinar` — boolean
    - `personalSettings` — UserPbxPersonalSettings
    - `dialplanSettings` — UserPbxDialplanSettings
    - `awsRegion` — string — The AWS region where the PBX is located.
    - `updatedAt` — string — The date when link data was updated last time.

**`BatchGetUsersPbxLinkDataV1RequestContent`**

- `id` — array **(required)** _(minItems=1; maxItems=500)_
  - _array of_ `string`

**`BatchGetUsersPbxLinkDataV1ResponseContent`**

- `users` — array **(required)**
  - _array of_ `UserPbxLinkData`
    - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
    - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
    - `companyName` — string — The name of the tenant (company) associated with the user.
    - `domain` — string **(required)** — The domain of the PBX where the user connected to.
    - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `info` — UserPersonalInfo **(required)**
      - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
      - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
      - `name` — string **(required)** — Name of the user (example: 'John Doe').
      - `extension` — string **(required)** — Extension number of the user (example: '111').
      - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
      - `role` — string **(required)** — Role of the user (example: 'admin').
      - `language` — string **(required)** — Language preference of the user (example: 'en').
      - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
      - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
      - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
      - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
      - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
      - `groupName` — string **(required)** — Name of the user's group.
      - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
      - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
      - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
      - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
      - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
      - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
      - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
    - `pbx` — UserPbxInfo **(required)**
      - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
        - _array of_ `string`
      - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
        - _array of_ `string`
      - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
      - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
      - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
    - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
    - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
    - `port` — string **(required)** — The port used for the PBX connection.
    - `serial` — string **(required)** — The serial number of the PBX.
    - `services` — UserPbxServices
      - `xcaracal` — boolean
      - `wizyWebinar` — boolean
    - `personalSettings` — UserPbxPersonalSettings
    - `dialplanSettings` — UserPbxDialplanSettings
    - `awsRegion` — string — The AWS region where the PBX is located.
    - `updatedAt` — string — The date when link data was updated last time.

**`BatchGetUsersRequestContent`**

- `id` — array **(required)** _(minItems=1; maxItems=500)_
  - _array of_ `string`

**`BatchGetUsersResponseContent`**

- `users` — array **(required)** — A list of users that exist in the platform.
  - _array of_ `User`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string

**`Bot`**

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `category` — string — Category of the bot _(minLen=1; maxLen=128)_
- `picture` — string — A link to the bot picture.
- `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
- `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
- `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
- `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
- `integrationApiKeysCount` — number **(required)**
- `createdAt` — string **(required)**
- `updated` — string

**`BotAccess`**

- string _(enum: `EVERYBODY`, `ORGANIZATION`)_

**`BotAlreadyExistsExceptionResponseContent`**

- `message` — string **(required)**

**`BotApiKey`**

- `secret` — string **(required)** _(minLen=96; maxLen=96)_
- `name` — string _(minLen=1; maxLen=64)_
- `createdAt` — string **(required)**

**`BotApiKeyNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`BotCallback`**

- `endpoint` — union
  - _oneOf_ — exactly one of:
    - **`llm`**
      - `llm` — BotLlmEndpoint **(required)**
        - `prompt` — string **(required)** _(maxLen=40000)_
        - `guidelines` — array
          - _array of_ `string`
        - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
        - `embeddedTools` — array — Embedded functions to use within chat session.
          - _(nesting depth limit — see `BotLlmEmbeddedTool` in the Schemas appendix)_
        - `tools` — array — Custom tools to be used within chat session.
          - _(nesting depth limit — see `BotLlmTool` in the Schemas appendix)_
        - `capabilities` — array
          - _(nesting depth limit — see `BotCapability` in the Schemas appendix)_
    - **`dialogflowCx`**
      - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
        - `credentials` — any **(required)** — Dialogflow Service Account Credentials
        - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
        - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
        - `language` — string **(required)** — Language
    - **`openAiAssistant`**
      - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
        - `key` — string **(required)**
        - `assistantId` — string **(required)**
    - **`webhook`**
      - `webhook` — BotWebhookEndpoint **(required)**
        - `url` — string **(required)**
        - `secret` — string **(required)**
    - **`sqs`**
      - `sqs` — BotSqsEndpoint **(required)**
        - `url` — string **(required)**
        - `key` — string **(required)**
        - `secret` — string **(required)**

**`BotCapability`**

- _oneOf_ — exactly one of:
  - **`tool`**
    - `tool` — BotCapabilityTool **(required)**
      - `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
      - `variables` — array
        - _array of_ `BotToolVariable`
          - _(nesting depth limit — see `BotToolVariable` in the Schemas appendix)_
      - `pipeline` — BotCapabilityToolPipeline
        - `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
        - `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.
      - `annotations` — array
        - _array of_ `BotToolAnnotation`
          - _(nesting depth limit — see `BotToolAnnotation` in the Schemas appendix)_
  - **`kb`**
    - `kb` — BotKnowledgeBase **(required)**
      - `knowledgeBaseId` — string
      - `instructions` — string — Additional instructions for when the bot should use this knowledge base.
      - `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
      - `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
      - `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
      - `annotations` — array
        - _array of_ `BotToolAnnotation`
          - _(nesting depth limit — see `BotToolAnnotation` in the Schemas appendix)_

**`BotCapabilityTool`**

- `id` — string **(required)** — Unique identifier of the tool using nanoid format _(pattern=^[0-9A-Za-z]{12}$; minLen=12; maxLen=12)_
- `variables` — array
  - _array of_ `BotToolVariable`
    - `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
    - `handler` — union
      - _oneOf_ — exactly one of:
        - **`auto`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`guided`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`predefined`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- `pipeline` — BotCapabilityToolPipeline
  - `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
  - `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.
- `annotations` — array
  - _array of_ `BotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — BotToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — BotToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — BotToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — BotToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`BotCapabilityToolPipeline`**

- `type` — string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_
- `instructions` — string — Instructions for generating a reply when using guided pipeline types. Use {{response}} to reference the tool response.

**`BotCapabilityToolPipelineType`**

- string _(enum: `blocking_request`, `blocking_request_guided`, `async_request`, `async_request_guided`)_

**`BotDialogflowCxEndpoint`**

- `credentials` — any **(required)** — Dialogflow Service Account Credentials
- `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
- `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
- `language` — string **(required)** — Language

**`BotEndpoint`**

- _oneOf_ — exactly one of:
  - **`llm`**
    - `llm` — BotLlmEndpoint **(required)**
      - `prompt` — string **(required)** _(maxLen=40000)_
      - `guidelines` — array
        - _array of_ `string`
      - `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
      - `embeddedTools` — array — Embedded functions to use within chat session.
        - _array of_ `BotLlmEmbeddedTool`
          - _(nesting depth limit — see `BotLlmEmbeddedTool` in the Schemas appendix)_
      - `tools` — array — Custom tools to be used within chat session.
        - _array of_ `BotLlmTool`
          - _(nesting depth limit — see `BotLlmTool` in the Schemas appendix)_
      - `capabilities` — array
        - _array of_ `BotCapability`
          - _(nesting depth limit — see `BotCapability` in the Schemas appendix)_
  - **`dialogflowCx`**
    - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
      - `credentials` — any **(required)** — Dialogflow Service Account Credentials
      - `agent` — string **(required)** — Dialogflow Agent Id (example - 88ff4635-0852-4f97-ae44-b19ae9fa6ea1
      - `location` — string **(required)** — Dialogflow Agent Region (example: europe-west3)
      - `language` — string **(required)** — Language
  - **`openAiAssistant`**
    - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
      - `key` — string **(required)**
      - `assistantId` — string **(required)**
  - **`webhook`**
    - `webhook` — BotWebhookEndpoint **(required)**
      - `url` — string **(required)**
      - `secret` — string **(required)**
  - **`sqs`**
    - `sqs` — BotSqsEndpoint **(required)**
      - `url` — string **(required)**
      - `key` — string **(required)**
      - `secret` — string **(required)**

**`BotIntegrationType`**

- string _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_

**`BotKnowledgeBase`**

- `knowledgeBaseId` — string
- `instructions` — string — Additional instructions for when the bot should use this knowledge base.
- `searchStrategy` — string _(enum: `bm25`, `vector`, `hybrid`)_
- `searchThreshold` — string _(enum: `low`, `medium`, `high`)_
- `searchLimit` — number — Maximum number of search results returned by this knowledge base capability. _(min=1; max=50)_
- `annotations` — array
  - _array of_ `BotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — BotToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — BotToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — BotToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — BotToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`BotLlmEmbeddedTool`**

- `type` — string **(required)** _(enum: `HANDOVER`, `DELEGATE`, `SUGGESTIONS`)_
- `name` — string **(required)**
- `parameters` — any — The parameters the functions accepts.
- `annotations` — array
  - _array of_ `BotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — BotToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — BotToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — BotToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — BotToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`BotLlmEmbeddedToolType`**

- string _(enum: `HANDOVER`, `DELEGATE`, `SUGGESTIONS`)_

**`BotLlmEndpoint`**

- `prompt` — string **(required)** _(maxLen=40000)_
- `guidelines` — array
  - _array of_ `string`
- `model` — string — The AI model to use for generating responses. If not specified, uses the default model. _(default=default; pattern=^(default|([a-z0-9][a-z0-9-]*://[a-zA-Z0-9._/-]+(\?[a-zA-Z0-9._&=%-]*)?))$)_
- `embeddedTools` — array — Embedded functions to use within chat session.
  - _array of_ `BotLlmEmbeddedTool`
    - `type` — string **(required)** _(enum: `HANDOVER`, `DELEGATE`, `SUGGESTIONS`)_
    - `name` — string **(required)**
    - `parameters` — any — The parameters the functions accepts.
    - `annotations` — array
      - _array of_ `BotToolAnnotation`
        - _(nesting depth limit — see `BotToolAnnotation` in the Schemas appendix)_
- `tools` — array — Custom tools to be used within chat session.
  - _array of_ `BotLlmTool`
    - `type` — string **(required)** _(enum: `function`)_
    - `function` — BotLlmFunctionDefinition
      - `name` — string **(required)** — The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
      - `description` — string — A description of what the function does, used by the model to choose when and how to call the function.
      - `parameters` — any — The parameters the functions accepts, described as a JSON Schema object.
      - `integration` — union
        - _(nesting depth limit — see `BotLlmFunctionIntegration` in the Schemas appendix)_
    - `annotations` — array
      - _array of_ `BotToolAnnotation`
        - _(nesting depth limit — see `BotToolAnnotation` in the Schemas appendix)_
- `capabilities` — array
  - _array of_ `BotCapability`
    - _oneOf_ — exactly one of:
      - **`tool`**
        - `tool` — BotCapabilityTool **(required)**
          - _(nesting depth limit — see `BotCapabilityTool` in the Schemas appendix)_
      - **`kb`**
        - `kb` — BotKnowledgeBase **(required)**
          - _(nesting depth limit — see `BotKnowledgeBase` in the Schemas appendix)_

**`BotLlmFunctionDefinition`**

- `name` — string **(required)** — The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
- `description` — string — A description of what the function does, used by the model to choose when and how to call the function.
- `parameters` — any — The parameters the functions accepts, described as a JSON Schema object.
- `integration` — union
  - _oneOf_ — exactly one of:
    - **`webhook`**
      - `webhook` — BotLlmFunctionIntegrationWebhook **(required)**
        - `url` — string **(required)**
        - `method` — string _(enum: `get`, `post`, `put`, `delete`, `patch`)_
        - `async` — boolean
        - `authorization` — union
          - _(nesting depth limit — see `BotLlmFunctionIntegrationWebhookAuthorization` in the Schemas appendix)_
        - `headers` — array
          - _(nesting depth limit — see `BotLlmFunctionIntegrationWebhookHeader` in the Schemas appendix)_
        - `timeout` — number — Timeout in milliseconds for the webhook request. _(default=10000; min=5000; max=120000)_
        - `parameters` — any

**`BotLlmFunctionIntegration`**

- _oneOf_ — exactly one of:
  - **`webhook`**
    - `webhook` — BotLlmFunctionIntegrationWebhook **(required)**
      - `url` — string **(required)**
      - `method` — string _(enum: `get`, `post`, `put`, `delete`, `patch`)_
      - `async` — boolean
      - `authorization` — union
        - _oneOf_ — exactly one of:
          - **`bearer`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`basic`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`oauth`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `headers` — array
        - _array of_ `BotLlmFunctionIntegrationWebhookHeader`
          - _(nesting depth limit — see `BotLlmFunctionIntegrationWebhookHeader` in the Schemas appendix)_
      - `timeout` — number — Timeout in milliseconds for the webhook request. _(default=10000; min=5000; max=120000)_
      - `parameters` — any

**`BotLlmFunctionIntegrationMethod`**

- string _(enum: `get`, `post`, `put`, `delete`, `patch`)_

**`BotLlmFunctionIntegrationWebhook`**

- `url` — string **(required)**
- `method` — string _(enum: `get`, `post`, `put`, `delete`, `patch`)_
- `async` — boolean
- `authorization` — union
  - _oneOf_ — exactly one of:
    - **`bearer`**
      - `bearer` — BotLlmFunctionIntegrationWebhookAuthorizationBearer **(required)**
        - `token` — string **(required)**
    - **`basic`**
      - `basic` — BotLlmFunctionIntegrationWebhookAuthorizationBasic **(required)**
        - `username` — string **(required)**
        - `password` — string **(required)**
    - **`oauth`**
      - `oauth` — BotLlmFunctionIntegrationWebhookAuthorizationOAuth **(required)**
        - `clientId` — string **(required)**
        - `clientSecret` — string **(required)**
        - `endpointUrl` — string **(required)**
        - `scope` — string
- `headers` — array
  - _array of_ `BotLlmFunctionIntegrationWebhookHeader`
    - `key` — string **(required)**
    - `value` — string **(required)**
- `timeout` — number — Timeout in milliseconds for the webhook request. _(default=10000; min=5000; max=120000)_
- `parameters` — any

**`BotLlmFunctionIntegrationWebhookAuthorization`**

- _oneOf_ — exactly one of:
  - **`bearer`**
    - `bearer` — BotLlmFunctionIntegrationWebhookAuthorizationBearer **(required)**
      - `token` — string **(required)**
  - **`basic`**
    - `basic` — BotLlmFunctionIntegrationWebhookAuthorizationBasic **(required)**
      - `username` — string **(required)**
      - `password` — string **(required)**
  - **`oauth`**
    - `oauth` — BotLlmFunctionIntegrationWebhookAuthorizationOAuth **(required)**
      - `clientId` — string **(required)**
      - `clientSecret` — string **(required)**
      - `endpointUrl` — string **(required)**
      - `scope` — string

**`BotLlmFunctionIntegrationWebhookAuthorizationBasic`**

- `username` — string **(required)**
- `password` — string **(required)**

**`BotLlmFunctionIntegrationWebhookAuthorizationBearer`**

- `token` — string **(required)**

**`BotLlmFunctionIntegrationWebhookAuthorizationOAuth`**

- `clientId` — string **(required)**
- `clientSecret` — string **(required)**
- `endpointUrl` — string **(required)**
- `scope` — string

**`BotLlmFunctionIntegrationWebhookHeader`**

- `key` — string **(required)**
- `value` — string **(required)**

**`BotLlmTool`**

- `type` — string **(required)** _(enum: `function`)_
- `function` — BotLlmFunctionDefinition
  - `name` — string **(required)** — The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.
  - `description` — string — A description of what the function does, used by the model to choose when and how to call the function.
  - `parameters` — any — The parameters the functions accepts, described as a JSON Schema object.
  - `integration` — union
    - _oneOf_ — exactly one of:
      - **`webhook`**
        - `webhook` — BotLlmFunctionIntegrationWebhook **(required)**
          - _(nesting depth limit — see `BotLlmFunctionIntegrationWebhook` in the Schemas appendix)_
- `annotations` — array
  - _array of_ `BotToolAnnotation`
    - _oneOf_ — exactly one of:
      - **`tag`**
        - `tag` — BotToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolTagAnnotation` in the Schemas appendix)_
      - **`comment`**
        - `comment` — BotToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
          - _(nesting depth limit — see `BotToolCommentAnnotation` in the Schemas appendix)_
      - **`variables`**
        - `variables` — BotToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
      - **`result`**
        - `result` — BotToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`BotLlmToolType`**

- string _(enum: `function`)_

**`BotNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`BotOpenAiAssistantEndpoint`**

- `key` — string **(required)**
- `assistantId` — string **(required)**

**`BotSessionTimeoutMinutes`**

- number _(enum: `15`, `30`, `60`, `120`)_

**`BotSqsEndpoint`**

- `url` — string **(required)**
- `key` — string **(required)**
- `secret` — string **(required)**

**`BotToolAnnotation`**

_Configuration for annotations emitted after a tool completes. Tag and comment annotations can provide a handlebars value, while variables and result annotations opt into logging runtime data._

- _oneOf_ — exactly one of:
  - **`tag`**
    - `tag` — BotToolTagAnnotation **(required)** — Tag annotation emitted after a tool completes.
      - `value` — string — Static handlebars expression resolved against bot variables and helpers.
      - `applyOnSuccess` — boolean — Apply when the tool succeeds.
      - `applyOnFailure` — boolean — Apply when the tool fails.
  - **`comment`**
    - `comment` — BotToolCommentAnnotation **(required)** — Comment annotation emitted after a tool completes.
      - `value` — string — Static handlebars expression resolved against bot variables and helpers.
      - `applyOnSuccess` — boolean — Apply when the tool succeeds.
      - `applyOnFailure` — boolean — Apply when the tool fails.
  - **`variables`**
    - `variables` — BotToolVariablesAnnotation **(required)** — Variables annotation emitted after a tool completes.
  - **`result`**
    - `result` — BotToolResultAnnotation **(required)** — Result annotation emitted after a tool completes.

**`BotToolCommentAnnotation`**

_Comment annotation emitted after a tool completes._

- `value` — string — Static handlebars expression resolved against bot variables and helpers.
- `applyOnSuccess` — boolean — Apply when the tool succeeds.
- `applyOnFailure` — boolean — Apply when the tool fails.

**`BotToolResultAnnotation`**

_Result annotation emitted after a tool completes._

- BotToolResultAnnotation

**`BotToolTagAnnotation`**

_Tag annotation emitted after a tool completes._

- `value` — string — Static handlebars expression resolved against bot variables and helpers.
- `applyOnSuccess` — boolean — Apply when the tool succeeds.
- `applyOnFailure` — boolean — Apply when the tool fails.

**`BotToolVariable`**

- `name` — string **(required)** — Name of the tool variable, e.g.: 'myvar' _(pattern=^[a-zA-Z0-9_]+$; minLen=1; maxLen=128)_
- `handler` — union
  - _oneOf_ — exactly one of:
    - **`auto`**
      - `auto` — BotToolVariableAutoHandler **(required)**
    - **`guided`**
      - `guided` — BotToolVariableGuidedHandler **(required)**
        - `description` — string **(required)** _(minLen=1; maxLen=1024)_
    - **`predefined`**
      - `predefined` — BotToolVariablePredefinedHandler **(required)**
        - `description` — string **(required)**

**`BotToolVariableAutoHandler`**

- BotToolVariableAutoHandler

**`BotToolVariableGuidedHandler`**

- `description` — string **(required)** _(minLen=1; maxLen=1024)_

**`BotToolVariableHandler`**

- _oneOf_ — exactly one of:
  - **`auto`**
    - `auto` — BotToolVariableAutoHandler **(required)**
  - **`guided`**
    - `guided` — BotToolVariableGuidedHandler **(required)**
      - `description` — string **(required)** _(minLen=1; maxLen=1024)_
  - **`predefined`**
    - `predefined` — BotToolVariablePredefinedHandler **(required)**
      - `description` — string **(required)**

**`BotToolVariablePredefinedHandler`**

- `description` — string **(required)**

**`BotToolVariablesAnnotation`**

_Variables annotation emitted after a tool completes._

- BotToolVariablesAnnotation

**`BotWebhookEndpoint`**

- `url` — string **(required)**
- `secret` — string **(required)**

**`ChangeUserEmailRequestContent`**

- `newData` — NewEmailData **(required)**
  - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `companyId` — string — By default, API expects that company id will be the same for both new and old emails. If no - this field should be provided _(minLen=3; maxLen=30)_
  - `pbxDomain` — string — Target PBX domain name for cases with few PBXes in one WMS-network
- `oldData` — OldEmailData **(required)**
  - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `companyId` — string — By default, API expects that company id will be the same for both new and old emails. If no - this field should be provided _(minLen=3; maxLen=30)_

**`ChangeUserEmailResponseContent`**

- `sfnArn` — string **(required)**

**`CreateAnonymousSessionRequestContent`**

- `name` — string **(required)** _(minLen=1; maxLen=50)_
- `captchaProof` — string **(required)** _(maxLen=4096)_
- `context` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`widgetId`**
      - `widgetId` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
    - **`channelId`**
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`CreateAnonymousSessionResponseContent`**

- `syntheticEmail` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_

**`CreateBotApiKeyRequestContent`**

- `name` — string _(minLen=1; maxLen=64)_

**`CreateBotApiKeyResponseContent`**

- `bot` — Bot **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `picture` — string — A link to the bot picture.
  - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
  - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
  - `integrationApiKeysCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `updated` — string
- `key` — BotApiKey **(required)**
  - `secret` — string **(required)** _(minLen=96; maxLen=96)_
  - `name` — string _(minLen=1; maxLen=64)_
  - `createdAt` — string **(required)**

**`CreateBotRequestContent`**

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `category` — string — Category of the bot _(minLen=1; maxLen=128)_
- `picture` — string — A link to the bot picture.
- `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
- `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
- `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
- `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
- `id` — string — Optional bot id. Omit to mint a random 12-character id. Supply a Wilma agent id (`a_` plus 10) so RNA search and conversation members share that id. Conflicts if the id already exists. _(minLen=12; maxLen=12)_
- `callback` — BotCallback **(required)**
  - `endpoint` — union
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — BotLlmEndpoint **(required)**
          - _(nesting depth limit — see `BotLlmEndpoint` in the Schemas appendix)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - _(nesting depth limit — see `BotDialogflowCxEndpoint` in the Schemas appendix)_
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - _(nesting depth limit — see `BotOpenAiAssistantEndpoint` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - _(nesting depth limit — see `BotWebhookEndpoint` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - _(nesting depth limit — see `BotSqsEndpoint` in the Schemas appendix)_

**`CreateBotResponseContent`**

- `bot` — Bot **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `picture` — string — A link to the bot picture.
  - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
  - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
  - `integrationApiKeysCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `updated` — string

**`CreateSystemBotRequestContent`**

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `picture` — string — A URL pointing to the bot's avatar.

**`CreateSystemBotResponseContent`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_

**`DirectoryItem`**

- `extension` — string **(required)**
- `name` — string **(required)**
- `department` — string
- `group` — string

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetAccountResponseContent`**

- `account` — Account **(required)**
  - `id` — string **(required)** — Unique identifier of the account. _(minLen=16; maxLen=16)_
  - `defaultWorkspace` — string — The ID of the default workspace, if any. _(minLen=12; maxLen=12)_
  - `primaryIdentity` — string — The identity value (email address or phone number in E.164).

**`GetAppVersionResponseContent`**

- `version` — string **(required)** _(pattern=^[0-9]+\.[0-9]+\.[0-9]+$)_

**`GetBotCallbackResponseContent`**

- `callback` — BotCallback **(required)**
  - `endpoint` — union
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — BotLlmEndpoint **(required)**
          - _(nesting depth limit — see `BotLlmEndpoint` in the Schemas appendix)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - _(nesting depth limit — see `BotDialogflowCxEndpoint` in the Schemas appendix)_
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - _(nesting depth limit — see `BotOpenAiAssistantEndpoint` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - _(nesting depth limit — see `BotWebhookEndpoint` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - _(nesting depth limit — see `BotSqsEndpoint` in the Schemas appendix)_

**`GetBotResponseContent`**

- `bot` — Bot **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `picture` — string — A link to the bot picture.
  - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
  - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
  - `integrationApiKeysCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `updated` — string

**`GetPbxColleaguesDir`**

- string _(enum: `asc`, `desc`)_

**`GetUserEmailNotificationsSettingsResponseContent`**

- `notifications` — UserEmailNotificationsSettings **(required)**
  - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
  - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.

**`GetUserPbxLinkDataResponseContent`**

- `user` — UserPbxLinkData **(required)**
  - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
  - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
  - `companyName` — string — The name of the tenant (company) associated with the user.
  - `domain` — string **(required)** — The domain of the PBX where the user connected to.
  - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `info` — UserPersonalInfo **(required)**
    - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
    - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
    - `name` — string **(required)** — Name of the user (example: 'John Doe').
    - `extension` — string **(required)** — Extension number of the user (example: '111').
    - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
    - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
    - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
    - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
    - `role` — string **(required)** — Role of the user (example: 'admin').
    - `language` — string **(required)** — Language preference of the user (example: 'en').
    - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
    - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
    - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
    - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
    - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
    - `groupName` — string **(required)** — Name of the user's group.
    - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
    - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
    - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
    - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
    - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
    - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
    - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
  - `pbx` — UserPbxInfo **(required)**
    - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
      - _array of_ `string`
    - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
      - _array of_ `string`
    - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
    - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
    - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
  - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
  - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
  - `port` — string **(required)** — The port used for the PBX connection.
  - `serial` — string **(required)** — The serial number of the PBX.
  - `services` — UserPbxServices
    - `xcaracal` — boolean
    - `wizyWebinar` — boolean
  - `personalSettings` — UserPbxPersonalSettings
  - `dialplanSettings` — UserPbxDialplanSettings
  - `awsRegion` — string — The AWS region where the PBX is located.
  - `updatedAt` — string — The date when link data was updated last time.

**`GetUserPbxLinkSuggestionResponseContent`**

- `suggestion` — UserPbxLinkSuggestion
  - `domain` — string **(required)** — A domain of the PBX that can be used to connect the user.
  - `port` — string **(required)** — A port of the PBX that can be used to connect the user.

**`GetUserPbxLinkSuggestionV1ResponseContent`**

- `suggestion` — UserPbxLinkSuggestion
  - `domain` — string **(required)** — A domain of the PBX that can be used to connect the user.
  - `port` — string **(required)** — A port of the PBX that can be used to connect the user.

**`GetUserResponseContent`**

- `user` — User **(required)**
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string

**`Identity`**

- `identity` — string **(required)** — The identity value (email address or phone number in E.164)
- `account` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- `verified` — boolean — Indicates if the identity is verified.

**`IntelligenceSearchResponseContent`**

- `items` — array **(required)**
  - _array of_ `DirectoryItem`
    - `extension` — string **(required)**
    - `name` — string **(required)**
    - `department` — string
    - `group` — string

**`InviteRequestContent`**

- `invitees` — array **(required)** — A list of users to invite. The list must contain between 1 and 20 users. _(minItems=1; maxItems=20)_
  - _array of_ `UserToInvite`
    - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
    - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.

**`InviteResponseContent`**

- `users` — array **(required)** — A list of users who were successfully invited. Each entry contains only id, name, email, phone, picture, company, pbxUserId, and locale.
  - _array of_ `InvitedUser`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string — Avatar URL. Notification emails render it as the sender's avatar.
    - `company` — string — Tenant id. Callers use it to tell a colleague from an external user.
    - `pbxUserId` — string — PBX user id of a colleague. A caller that already knows the colleague matches the invite result by this value.
    - `locale` — string — Preferred user language. Notification emails sent to the invitee use it to pick the template language.
- `skippedInvitees` — array **(required)** — A list of invitees that were skipped during the operation, for example because the resolved account is deactivated in GetStream. Each entry carries the email or phone supplied in the request, and the user id when it was already known.
  - _array of_ `SkippedMember`
    - `id` — string — The unique identifier of the skipped user if it is known. _(minLen=12; maxLen=12)_
    - `email` — string — The email address of the skipped user if it is known. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the skipped user if it is known. _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_

**`InvitedUser`**

_Reduced user record returned by Invite. Callers receive only the fields they use to correlate the invitee and continue the conversation flow: id, name, email, phone, picture, company, pbxUserId, and locale. PBX installation details (domain, port, extension, serial, group), profile metadata (time zone, bot), and timestamps are not included._

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string
- `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string
- `picture` — string — Avatar URL. Notification emails render it as the sender's avatar.
- `company` — string — Tenant id. Callers use it to tell a colleague from an external user.
- `pbxUserId` — string — PBX user id of a colleague. A caller that already knows the colleague matches the invite result by this value.
- `locale` — string — Preferred user language. Notification emails sent to the invitee use it to pick the template language.

**`LinkIdentityRequestContent`**

- `identity` — string **(required)** — The identity value: email address or phone number in E.164.

**`LinkIdentityResponseContent`**

- `identity` — Identity **(required)**
  - `identity` — string **(required)** — The identity value (email address or phone number in E.164)
  - `account` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
  - `verified` — boolean — Indicates if the identity is verified.

**`ListBotApiKeysResponseContent`**

- `keys` — array **(required)**
  - _array of_ `BotApiKey`
    - `secret` — string **(required)** _(minLen=96; maxLen=96)_
    - `name` — string _(minLen=1; maxLen=64)_
    - `createdAt` — string **(required)**

**`ListBotsResponseContent`**

- `bots` — array **(required)**
  - _array of_ `Bot`
    - `name` — string **(required)** _(minLen=3; maxLen=255)_
    - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
    - `picture` — string — A link to the bot picture.
    - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
    - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
    - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
    - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
    - `integrationApiKeysCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `updated` — string

**`ListIdentitiesResponseContent`**

- `identities` — array **(required)**
  - _array of_ `Identity`
    - `identity` — string **(required)** — The identity value (email address or phone number in E.164)
    - `account` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
    - `verified` — boolean — Indicates if the identity is verified.

**`ListWorkspacesResponseContent`**

- `workspaces` — array **(required)** — Workspaces for this request. A paged response contains only active work workspaces, ordered with the account default first, then workspaces the user linked to before (most recent first), then the rest by domain.
  - _array of_ `Workspace`
    - `companyId` — string — The unique identifier of the tenant (company). _(minLen=3; maxLen=30)_
    - `pbxUser` — UserPbxLinkData
      - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
      - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
      - `companyName` — string — The name of the tenant (company) associated with the user.
      - `domain` — string **(required)** — The domain of the PBX where the user connected to.
      - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `info` — UserPersonalInfo **(required)**
        - _(nesting depth limit — see `UserPersonalInfo` in the Schemas appendix)_
      - `pbx` — UserPbxInfo **(required)**
        - _(nesting depth limit — see `UserPbxInfo` in the Schemas appendix)_
      - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
      - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
      - `port` — string **(required)** — The port used for the PBX connection.
      - `serial` — string **(required)** — The serial number of the PBX.
      - `services` — UserPbxServices
        - _(nesting depth limit — see `UserPbxServices` in the Schemas appendix)_
      - `personalSettings` — UserPbxPersonalSettings
      - `dialplanSettings` — UserPbxDialplanSettings
      - `awsRegion` — string — The AWS region where the PBX is located.
      - `updatedAt` — string — The date when link data was updated last time.
    - `streamUser` — User
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
    - `type` — string _(enum: `personal`, `work`, `support`)_
    - `id` — string **(required)** — The unique identifier _(minLen=12; maxLen=12)_
    - `accountId` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
    - `active` — boolean **(required)** — Indicates if the workspace is active.
- `total` — number — Number of selectable workspaces (active and type work) that match query, ignoring offset. Present when limit is set.

**`NewEmailData`**

- `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `companyId` — string — By default, API expects that company id will be the same for both new and old emails. If no - this field should be provided _(minLen=3; maxLen=30)_
- `pbxDomain` — string — Target PBX domain name for cases with few PBXes in one WMS-network

**`OldEmailData`**

- `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `companyId` — string — By default, API expects that company id will be the same for both new and old emails. If no - this field should be provided _(minLen=3; maxLen=30)_

**`PartialUpdateUserEmailNotificationsSettingsRequestContent`**

- `unread` — boolean — A flag that indicates whether the system should send email notifications about unread messages.
- `transcription` — boolean — A flag that indicates whether the system should send email notifications about AI transcription.

**`PartialUpdateUserEmailNotificationsSettingsResponseContent`**

- `notifications` — UserEmailNotificationsSettings **(required)**
  - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
  - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.

**`PbxColleague`**

- `id` — string **(required)**
- `name` — string
- `login` — string
- `extension` — string **(required)**
- `officePhone` — string
- `mobilePhone` — string
- `faxNumber` — string
- `email` — string
- `pbxDn` — string **(required)**
- `pbx` — string **(required)**
- `role` — string **(required)** _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
- `groupName` — string **(required)**
- `groupDn` — string **(required)**
- `language` — string **(required)**
- `dialplan` — string **(required)**
- `faxDialplan` — string **(required)**
- `department` — string
- `picture` — string **(required)**
- `sourceId` — string
- `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- `jid` — string **(required)**

**`PbxColleagueRole`**

- string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_

**`PbxColleaguesQueryField`**

- string _(enum: `extension`, `officePhone`, `mobilePhone`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, `login`, … (+5))_

**`PbxColleaguesSearchStrategy`**

- string _(enum: `contain`, `startsWith`)_

**`PbxLicenseType`**

- string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`QueryColleaguesOutputItem`**

- `user` — User
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string
- `colleague` — PbxColleague **(required)**
  - `id` — string **(required)**
  - `name` — string
  - `login` — string
  - `extension` — string **(required)**
  - `officePhone` — string
  - `mobilePhone` — string
  - `faxNumber` — string
  - `email` — string
  - `pbxDn` — string **(required)**
  - `pbx` — string **(required)**
  - `role` — string **(required)** _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
  - `groupName` — string **(required)**
  - `groupDn` — string **(required)**
  - `language` — string **(required)**
  - `dialplan` — string **(required)**
  - `faxDialplan` — string **(required)**
  - `department` — string
  - `picture` — string **(required)**
  - `sourceId` — string
  - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
  - `jid` — string **(required)**

**`QueryColleaguesParameters`**

- `id` — array
  - _array of_ `string`
- `extension` — array
  - _array of_ `string`
- `officePhone` — array
  - _array of_ `string`
- `mobilePhone` — array
  - _array of_ `string`
- `name` — array
  - _array of_ `string`
- `email` — array
  - _array of_ `string`
- `department` — array
  - _array of_ `string`
- `search` — string
- `searchFields` — array
  - _array of_ `PbxColleaguesQueryField`
- `searchStrategy` — string _(enum: `contain`, `startsWith`)_
- `sort` — array
  - _array of_ `PbxColleaguesQueryField`
- `start` — number
- `count` — number _(default=50; min=1; max=50)_
- `dir` — string _(enum: `asc`, `desc`)_

**`QueryColleaguesRequestContent`**

- `query` — QueryColleaguesParameters
  - `id` — array
    - _array of_ `string`
  - `extension` — array
    - _array of_ `string`
  - `officePhone` — array
    - _array of_ `string`
  - `mobilePhone` — array
    - _array of_ `string`
  - `name` — array
    - _array of_ `string`
  - `email` — array
    - _array of_ `string`
  - `department` — array
    - _array of_ `string`
  - `search` — string
  - `searchFields` — array
    - _array of_ `PbxColleaguesQueryField`
  - `searchStrategy` — string _(enum: `contain`, `startsWith`)_
  - `sort` — array
    - _array of_ `PbxColleaguesQueryField`
  - `start` — number
  - `count` — number _(default=50; min=1; max=50)_
  - `dir` — string _(enum: `asc`, `desc`)_
- `invite` — boolean — If enabled, the system will automatically invite users for colleagues returned from the PBX if they haven't logged in yet.

**`QueryColleaguesResponseContent`**

- `colleagues` — array **(required)** — A list of users that exist in the platform and matches predicate if specified.
  - _array of_ `QueryColleaguesOutputItem`
    - `user` — User
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxDomain` — string
      - `pbxPort` — string
      - `pbxExtension` — string
      - `pbxSerial` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
    - `colleague` — PbxColleague **(required)**
      - `id` — string **(required)**
      - `name` — string
      - `login` — string
      - `extension` — string **(required)**
      - `officePhone` — string
      - `mobilePhone` — string
      - `faxNumber` — string
      - `email` — string
      - `pbxDn` — string **(required)**
      - `pbx` — string **(required)**
      - `role` — string **(required)** _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
      - `groupName` — string **(required)**
      - `groupDn` — string **(required)**
      - `language` — string **(required)**
      - `dialplan` — string **(required)**
      - `faxDialplan` — string **(required)**
      - `department` — string
      - `picture` — string **(required)**
      - `sourceId` — string
      - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
      - `jid` — string **(required)**

**`QueryUserRequestContent`**

- `query` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`id`**
      - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX).
    - **`email`**
      - `email` — string **(required)** — The email address of the user.
    - **`phone`**
      - `phone` — string **(required)** — The phone number of the user.
- `predicate` — UserQueryPredicate
  - `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`QueryUserResponseContent`**

- `user` — User **(required)**
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string

**`QueryUsersRequestContent`**

- `queries` — array **(required)** _(minItems=1; maxItems=50)_
  - _array of_ `UserQuery`
    - _oneOf_ — exactly one of:
      - **`id`**
        - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX).
      - **`email`**
        - `email` — string **(required)** — The email address of the user.
      - **`phone`**
        - `phone` — string **(required)** — The phone number of the user.
- `predicate` — UserQueryPredicate
  - `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`QueryUsersResponseContent`**

- `users` — array **(required)** — A list of users that exist in the platform and matches predicate if specified.
  - _array of_ `User`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string

**`RateLimitExceededExceptionResponseContent`**

- `message` — string **(required)** _(default=Too Many Requests)_

**`SearchStrategy`**

- string _(enum: `bm25`, `vector`, `hybrid`)_

**`SearchThresholdValue`**

- string _(enum: `low`, `medium`, `high`)_

**`SkippedMember`**

- `id` — string — The unique identifier of the skipped user if it is known. _(minLen=12; maxLen=12)_
- `email` — string — The email address of the skipped user if it is known. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string — The phone number of the skipped user if it is known. _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_

**`ToggleTranscriptionEmailNotificationsSubscriptionRequestContent`**

- `unsubscribeToken` — string **(required)**
- `subscribe` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.

**`ToggleUnreadEmailNotificationsSubscriptionRequestContent`**

- `unsubscribeToken` — string **(required)**
- `subscribe` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.

**`UpdateAccountRequestContent`**

- `defaultWorkspace` — string — The workspace to set as default. _(minLen=12; maxLen=12)_
- `primaryIdentity` — string — The identity value (email or phone) to set as primary.

**`UpdateAccountResponseContent`**

- `account` — Account **(required)**
  - `id` — string **(required)** — Unique identifier of the account. _(minLen=16; maxLen=16)_
  - `defaultWorkspace` — string — The ID of the default workspace, if any. _(minLen=12; maxLen=12)_
  - `primaryIdentity` — string — The identity value (email address or phone number in E.164).

**`UpdateBotCallbackRequestContent`**

- `callback` — BotCallback **(required)**
  - `endpoint` — union
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — BotLlmEndpoint **(required)**
          - _(nesting depth limit — see `BotLlmEndpoint` in the Schemas appendix)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - _(nesting depth limit — see `BotDialogflowCxEndpoint` in the Schemas appendix)_
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - _(nesting depth limit — see `BotOpenAiAssistantEndpoint` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - _(nesting depth limit — see `BotWebhookEndpoint` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - _(nesting depth limit — see `BotSqsEndpoint` in the Schemas appendix)_

**`UpdateBotCallbackResponseContent`**

- `callback` — BotCallback **(required)**
  - `endpoint` — union
    - _oneOf_ — exactly one of:
      - **`llm`**
        - `llm` — BotLlmEndpoint **(required)**
          - _(nesting depth limit — see `BotLlmEndpoint` in the Schemas appendix)_
      - **`dialogflowCx`**
        - `dialogflowCx` — BotDialogflowCxEndpoint **(required)**
          - _(nesting depth limit — see `BotDialogflowCxEndpoint` in the Schemas appendix)_
      - **`openAiAssistant`**
        - `openAiAssistant` — BotOpenAiAssistantEndpoint **(required)**
          - _(nesting depth limit — see `BotOpenAiAssistantEndpoint` in the Schemas appendix)_
      - **`webhook`**
        - `webhook` — BotWebhookEndpoint **(required)**
          - _(nesting depth limit — see `BotWebhookEndpoint` in the Schemas appendix)_
      - **`sqs`**
        - `sqs` — BotSqsEndpoint **(required)**
          - _(nesting depth limit — see `BotSqsEndpoint` in the Schemas appendix)_

**`UpdateBotRequestContent`**

- `name` — string **(required)** _(minLen=3; maxLen=255)_
- `category` — string — Category of the bot _(minLen=1; maxLen=128)_
- `picture` — string — A link to the bot picture.
- `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
- `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
- `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
- `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_

**`UpdateBotResponseContent`**

- `bot` — Bot **(required)**
  - `name` — string **(required)** _(minLen=3; maxLen=255)_
  - `category` — string — Category of the bot _(minLen=1; maxLen=128)_
  - `picture` — string — A link to the bot picture.
  - `searchable` — boolean — Indicates whether the bot can be discovered by colleagues in the application.
  - `access` — string _(enum: `EVERYBODY`, `ORGANIZATION`)_
  - `groupId` — string — PBX group ID for ACL-based visibility in Sales Intelligence.
  - `sessionTimeoutMinutes` — number _(enum: `15`, `30`, `60`, `120`)_
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `integrationType` — string **(required)** _(enum: `LLM`, `DIALOGFLOW_CX`, `OPEN_AI_ASSISTANT`, `WEBHOOK`, `SQS`)_
  - `integrationApiKeysCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `updated` — string

**`UpdateUserEmailNotificationsSettingsRequestContent`**

- `unread` — boolean — A flag that indicates whether the system should send email notifications about unread messages.
- `transcription` — boolean — A flag that indicates whether the system should send email notifications about AI transcription.

**`UpdateUserEmailNotificationsSettingsResponseContent`**

- `notifications` — UserEmailNotificationsSettings **(required)**
  - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
  - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.

**`UpdateWorkspaceRequestContent`**

- `active` — boolean — Indicates if the workspace is active.
- `type` — string _(enum: `personal`, `work`, `support`)_

**`UpdateWorkspaceResponseContent`**

- `workspace` — Workspace **(required)**
  - `companyId` — string — The unique identifier of the tenant (company). _(minLen=3; maxLen=30)_
  - `pbxUser` — UserPbxLinkData
    - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
    - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
    - `companyName` — string — The name of the tenant (company) associated with the user.
    - `domain` — string **(required)** — The domain of the PBX where the user connected to.
    - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `info` — UserPersonalInfo **(required)**
      - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
      - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
      - `name` — string **(required)** — Name of the user (example: 'John Doe').
      - `extension` — string **(required)** — Extension number of the user (example: '111').
      - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
      - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
      - `role` — string **(required)** — Role of the user (example: 'admin').
      - `language` — string **(required)** — Language preference of the user (example: 'en').
      - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
      - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
      - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
      - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
      - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
      - `groupName` — string **(required)** — Name of the user's group.
      - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
      - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
      - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
      - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
      - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
      - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
      - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
    - `pbx` — UserPbxInfo **(required)**
      - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
        - _array of_ `string`
      - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
        - _array of_ `string`
      - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
      - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
      - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
    - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
    - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
    - `port` — string **(required)** — The port used for the PBX connection.
    - `serial` — string **(required)** — The serial number of the PBX.
    - `services` — UserPbxServices
      - `xcaracal` — boolean
      - `wizyWebinar` — boolean
    - `personalSettings` — UserPbxPersonalSettings
    - `dialplanSettings` — UserPbxDialplanSettings
    - `awsRegion` — string — The AWS region where the PBX is located.
    - `updatedAt` — string — The date when link data was updated last time.
  - `streamUser` — User
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxDomain` — string
    - `pbxPort` — string
    - `pbxExtension` — string
    - `pbxSerial` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
  - `type` — string _(enum: `personal`, `work`, `support`)_
  - `id` — string **(required)** — The unique identifier _(minLen=12; maxLen=12)_
  - `accountId` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
  - `active` — boolean **(required)** — Indicates if the workspace is active.

**`UploadPictureRequestContent`**

- `picture` — string **(required)** — A base64 encoded image file in PNG or JPG format, with dimensions of 140 x 140 pixels.

**`UploadPictureResponseContent`**

- `url` — string **(required)**

**`UploadPictureV1RequestContent`**

- `picture` — string **(required)** — A base64 encoded image file in PNG or JPG format, with dimensions of 140 x 140 pixels.

**`UploadPictureV1ResponseContent`**

- `url` — string **(required)**

**`User`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string
- `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string
- `picture` — string
- `locale` — string
- `timeZone` — string
- `company` — string
- `bot` — boolean
- `pbxDomain` — string
- `pbxPort` — string
- `pbxExtension` — string
- `pbxSerial` — string
- `pbxUserId` — string
- `pbxGroupId` — string
- `createdAt` — string
- `updatedAt` — string

**`UserEmailNotificationsSettings`**

- `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
- `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.

**`UserNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`UserPbxDialplanSettings`**

- UserPbxDialplanSettings

**`UserPbxInfo`**

- `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
  - _array of_ `string`
- `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
  - _array of_ `string`
- `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
- `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
- `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').

**`UserPbxLinkData`**

- `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
- `company` — string **(required)** — The ID of the tenant (company) associated with the user.
- `companyName` — string — The name of the tenant (company) associated with the user.
- `domain` — string **(required)** — The domain of the PBX where the user connected to.
- `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `info` — UserPersonalInfo **(required)**
  - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
  - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
  - `name` — string **(required)** — Name of the user (example: 'John Doe').
  - `extension` — string **(required)** — Extension number of the user (example: '111').
  - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
  - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
  - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
  - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
  - `role` — string **(required)** — Role of the user (example: 'admin').
  - `language` — string **(required)** — Language preference of the user (example: 'en').
  - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
  - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
  - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
  - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
  - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
  - `groupName` — string **(required)** — Name of the user's group.
  - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
  - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
  - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
  - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
  - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
  - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
  - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
- `pbx` — UserPbxInfo **(required)**
  - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
    - _array of_ `string`
  - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
    - _array of_ `string`
  - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
  - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
  - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
- `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
- `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
- `port` — string **(required)** — The port used for the PBX connection.
- `serial` — string **(required)** — The serial number of the PBX.
- `services` — UserPbxServices
  - `xcaracal` — boolean
  - `wizyWebinar` — boolean
- `personalSettings` — UserPbxPersonalSettings
- `dialplanSettings` — UserPbxDialplanSettings
- `awsRegion` — string — The AWS region where the PBX is located.
- `updatedAt` — string — The date when link data was updated last time.

**`UserPbxLinkSuggestion`**

- `domain` — string **(required)** — A domain of the PBX that can be used to connect the user.
- `port` — string **(required)** — A port of the PBX that can be used to connect the user.

**`UserPbxPersonalSettings`**

- UserPbxPersonalSettings

**`UserPbxServices`**

- `xcaracal` — boolean
- `wizyWebinar` — boolean

**`UserPersonalInfo`**

- `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
- `id` — string **(required)** — Unique identifier of the user (example: '9010198').
- `name` — string **(required)** — Name of the user (example: 'John Doe').
- `extension` — string **(required)** — Extension number of the user (example: '111').
- `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
- `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
- `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
- `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
- `role` — string **(required)** — Role of the user (example: 'admin').
- `language` — string **(required)** — Language preference of the user (example: 'en').
- `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
- `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
- `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
- `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
- `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
- `groupName` — string **(required)** — Name of the user's group.
- `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
- `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
- `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
- `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
- `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
- `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.

**`UserQuery`**

- _oneOf_ — exactly one of:
  - **`id`**
    - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX).
  - **`email`**
    - `email` — string **(required)** — The email address of the user.
  - **`phone`**
    - `phone` — string **(required)** — The phone number of the user.

**`UserQueryPredicate`**

- `license` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`UserToInvite`**

- `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
- `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.

**`UsersEmailNotificationsSettingsMap`**

- _map of_ `UserEmailNotificationsSettings`
  - `unread` — boolean **(required)** — A flag that indicates whether the system should send email notifications about unread messages.
  - `transcription` — boolean **(required)** — A flag that indicates whether the system should send email notifications about AI transcription.

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`VerifyBotSecretKeyRequestContent`**

- `secret` — string **(required)** — A secret key string with "sk-" _(minLen=96; maxLen=96)_

**`VerifyBotSecretKeyResponseContent`**

- `company` — string **(required)**
- `id` — string **(required)** — A unique ID for the Bot that corresponds to the bot's x-bees user ID. _(minLen=12; maxLen=12)_
- `name` — string _(minLen=1; maxLen=64)_

**`VerifyBotSecretKeyV1RequestContent`**

- `secret` — string **(required)** — A secret key string with "sk-" _(minLen=96; maxLen=96)_

**`VerifyBotSecretKeyV1ResponseContent`**

- `company` — string **(required)**
- `id` — string **(required)** — A unique ID for the Bot that corresponds to the bot's x-bees user ID. _(minLen=12; maxLen=12)_
- `name` — string _(minLen=1; maxLen=64)_

**`VerifyIdentityRequestContent`**

- `identity` — string **(required)** — The identity value that was added (email or phone).
- `otp` — string **(required)** — OTP sent to the new identity to prove ownership.

**`VerifyIdentityResponseContent`**

- `identity` — Identity **(required)**
  - `identity` — string **(required)** — The identity value (email address or phone number in E.164)
  - `account` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
  - `verified` — boolean — Indicates if the identity is verified.

**`WidgetNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`Workspace`**

- `companyId` — string — The unique identifier of the tenant (company). _(minLen=3; maxLen=30)_
- `pbxUser` — UserPbxLinkData
  - `id` — string **(required)** — The unique identifier of the user (Cloud ID, not ID of the user on PBX). _(minLen=12; maxLen=12)_
  - `company` — string **(required)** — The ID of the tenant (company) associated with the user.
  - `companyName` — string — The name of the tenant (company) associated with the user.
  - `domain` — string **(required)** — The domain of the PBX where the user connected to.
  - `email` — string — The email address of the user. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `info` — UserPersonalInfo **(required)**
    - `dn` — string **(required)** — Distinguished Name (DN) of the user in the directory (example: 'uid=9010198,o=com0,dc=wildix').
    - `id` — string **(required)** — Unique identifier of the user (example: '9010198').
    - `name` — string **(required)** — Name of the user (example: 'John Doe').
    - `extension` — string **(required)** — Extension number of the user (example: '111').
    - `officePhone` — string — Office phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
    - `mobilePhone` — string — Mobile phone number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
    - `faxNumber` — string — Fax number of the user (example: '22222'). This field can be an empty string or undefined if not provided.
    - `email` — string — Email address of the user (example: 'email@google.com'). This field can be an empty string or undefined if not provided.
    - `role` — string **(required)** — Role of the user (example: 'admin').
    - `language` — string **(required)** — Language preference of the user (example: 'en').
    - `dialplan` — string **(required)** — Dialplan associated with the user (example: 'users').
    - `faxDialplan` — string **(required)** — Fax dialplan associated with the user. Example: 'users'.
    - `departament` — string — Department of the user (example: 'Sales'). This field can be an empty string or undefined if not provided.
    - `picture` — string **(required)** — Public URL path of the user's picture (example: '/cticonnect/cticonnect_share/user_avatar_3688190.png?100&John Doe&98998generated').
    - `groupDn` — string **(required)** — Distinguished Name (DN) of the user's group in the directory. Example: 'gid=5194383,o=com0,dc=wildix'.
    - `groupName` — string **(required)** — Name of the user's group.
    - `jid` — string **(required)** — Jabber ID (JID) of the user. Example: '100@example.wildixin.com'.
    - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
    - `login` — string — Login name of the user. This field can be an empty string or undefined if not provided.
    - `pbx` — string — PBX associated with the user. This field can be an empty string or undefined if not provided.
    - `pbxDn` — string **(required)** — Distinguished Name (DN) of the PBX associated with the user. Example: 'pbxid=0800276a7b26,dc=wildix'.
    - `sourceId` — string — Source identifier for the user's authorization (example: '117868550326216144929').
    - `sipPassword` — string — SIP password for the user, used to authenticate and secure SIP communications such as VoIP calls.
  - `pbx` — UserPbxInfo **(required)**
    - `networkAddresses` — array **(required)** — Network addresses associated with the PBX (example: ['krzhevitskywms4.wildixin.com']).
      - _array of_ `string`
    - `ports` — array **(required)** — Specifies the HTTPs ports utilized by the PBX system (example: ['443']).
      - _array of_ `string`
    - `externalLinePrefix` — string — Prefix used for external lines (eample: '0').
    - `version` — string **(required)** — Version of the PBX software (example: '5.03.20210820.2~67439e5d').
    - `serial` — string **(required)** — Serial number of the PBX (example: '221100002aa2').
  - `picture` — string **(required)** — A public URL of the user's picture (example: https://example.wildixin.com/cticonnect/cticonnect_share/user_avatar_3688190.png)
  - `pictureDeleted` — boolean — Indicates whether the picture was manually removed by the user. If true the application must show a placeholder instead of the default picture from the PBX.
  - `port` — string **(required)** — The port used for the PBX connection.
  - `serial` — string **(required)** — The serial number of the PBX.
  - `services` — UserPbxServices
    - `xcaracal` — boolean
    - `wizyWebinar` — boolean
  - `personalSettings` — UserPbxPersonalSettings
  - `dialplanSettings` — UserPbxDialplanSettings
  - `awsRegion` — string — The AWS region where the PBX is located.
  - `updatedAt` — string — The date when link data was updated last time.
- `streamUser` — User
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `name` — string
  - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string
  - `picture` — string
  - `locale` — string
  - `timeZone` — string
  - `company` — string
  - `bot` — boolean
  - `pbxDomain` — string
  - `pbxPort` — string
  - `pbxExtension` — string
  - `pbxSerial` — string
  - `pbxUserId` — string
  - `pbxGroupId` — string
  - `createdAt` — string
  - `updatedAt` — string
- `type` — string _(enum: `personal`, `work`, `support`)_
- `id` — string **(required)** — The unique identifier _(minLen=12; maxLen=12)_
- `accountId` — string **(required)** — The unique identifier of the account. _(minLen=16; maxLen=16)_
- `active` — boolean **(required)** — Indicates if the workspace is active.

**`WorkspaceNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`WorkspaceType`**

- string _(enum: `personal`, `work`, `support`)_

</details>
