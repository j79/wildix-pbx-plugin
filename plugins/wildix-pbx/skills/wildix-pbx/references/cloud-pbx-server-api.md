## Cloud PBX Server API

_OpenAPI: WMS server service — version —_

**Servers**

- `https://{domain}.wildixin.com` — 

### Colleagues

#### `GET` `/api/v1/Colleagues/{id}/`

- operationId: `GetColleagueById`
- **Parameters**
  - `id` (path) — number **(required)**
- **Response 200** (`GetColleagueByIdResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — PbxColleague **(required)**
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
- Errors: `401`, `403`

#### `GET` `/api/v1/PBX/Colleagues`

- operationId: `GetPbxColleagues`
- **Parameters**
  - `filter[extension][]` (query) — array
  - `filter[id][]` (query) — array
  - `filter[officePhone][]` (query) — array
  - `filter[mobilePhone][]` (query) — array
  - `filter[name][]` (query) — array
  - `filter[email][]` (query) — array
  - `filter[role][]` (query) — array
  - `filter[dialplan][]` (query) — array
  - `filter[faxDialplan][]` (query) — array
  - `filter[department][]` (query) — array
  - `filter[login][]` (query) — array
  - `filter[groupDn][]` (query) — array
  - `filter[pbxDn][]` (query) — array
  - `filter[licenseType][]` (query) — array
  - `fields` (query) — array
  - `searchFields` (query) — array
  - `search` (query) — string
  - `sort` (query) — array — The field to sort by. The PBX sorts by one field: pass a single item. The list is sent as a repeated parameter and the PBX reads only the last one, so it is deliberately not `@commaDelimited`.
  - `start` (query) — number
  - `count` (query) — number
  - `dir` (query) — string _(enum: `asc`, `desc`)_
  - `searchStrategy` (query) — string _(enum: `contain`, `startsWith`)_
- **Response 200** (`GetPbxColleaguesResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — GetPbxColleaguesResult **(required)**
    - `records` — array **(required)**
      - _array of_ `PbxColleague`
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
    - `total` — number **(required)**
- Errors: `401`, `403`

#### `POST` `/api/v1/PBX/Colleagues`

- operationId: `CreatePbxColleague`
- **Request body** (`application/json` — `CreatePbxColleagueRequestContent`) **(required)**
  - `extension` — string **(required)**
  - `name` — string **(required)**
  - `officePhone` — string
  - `mobilePhone` — string
  - `faxNumber` — string
  - `email` — string
  - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
  - `groupDn` — string
  - `language` — string
  - `dialplan` — string
  - `faxDialplan` — string
  - `department` — string
  - `login` — string
  - `password` — string
  - `sipPassword` — string
  - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- **Response 200** (`CreatePbxColleagueResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — PbxColleague **(required)**
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
- Errors: `401`, `403`

#### `PUT` `/api/v1/PBX/Colleagues/{id}`

- operationId: `UpdatePbxColleague`
- **Parameters**
  - `id` (path) — number **(required)**
- **Request body** (`application/json` — `UpdatePbxColleagueRequestContent`)
  - `extension` — string
  - `name` — string
  - `officePhone` — string
  - `mobilePhone` — string
  - `faxNumber` — string
  - `email` — string
  - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
  - `groupDn` — string
  - `language` — string
  - `dialplan` — string
  - `faxDialplan` — string
  - `department` — string
  - `login` — string
  - `password` — string
  - `sipPassword` — string
  - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
  - `picture` — string
- **Response 200** (`UpdatePbxColleagueResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — PbxColleague **(required)**
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
- Errors: `401`, `403`

#### `DELETE` `/api/v1/PBX/Colleagues/{id}`

- operationId: `DeletePbxColleague`
- **Parameters**
  - `id` (path) — number **(required)**
- **Response 200** (`DeletePbxColleagueResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — string **(required)** _(default=Success)_
- Errors: `401`, `403`

### Departments

#### `GET` `/api/v1/Departments/`

- operationId: `GetDepartments`
- **Response 200** (`GetDepartmentsResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — GetDepartmentsResult **(required)**
    - `records` — array **(required)**
      - _array of_ `PbxDepartment`
        - `id` — string **(required)** — Department id.
        - `name` — string **(required)** — Department name.
        - `users` — array — User extensions in this department.
          - _array of_ `string`
        - `items` — array — Child departments (recursive).
          - _array of_ `PbxDepartment`
            - _(nesting depth limit — see `PbxDepartment` in the Schemas appendix)_
- Errors: `401`, `403`

### Groups

#### `GET` `/api/v1/Dialplan/CallGroups/`

Get the list of all available Call groups on the PBX.

- operationId: `GetPbxCallGroups`
- **Response 200** (`GetPbxCallGroupsResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — GetPbxCallGroupsResult **(required)**
    - `records` — array **(required)**
      - _array of_ `PbxCallGroup`
        - `id` — number **(required)**
        - `title` — string **(required)**
        - `members` — array **(required)**
          - _array of_ `string`
        - `settings` — PbxCallGroupSettings **(required)**
          - `queueManager` — string
          - `cid` — string
          - `autoPause` — string
          - `autoPauseTime` — number
          - `autoPauseDelay` — number
          - `autoPauseBusy` — boolean
          - `autoPauseUnAvail` — boolean
          - `maxLen` — number
          - `retry` — number
          - `ringInUse` — boolean
          - `strategy` — string
          - `defaultPriority` — number
          - `timeout` — number
          - `weight` — number
          - `wrapUpTime` — number
          - `rule` — string
          - `announce` — PbxCallGroupAnnounce
            - `frequency` — number
            - `holdTime` — string
            - `roundSeconds` — number
          - `exitAllMembers` — PbxCallGroupExitAllMembers
            - `busy` — boolean
            - `paused` — boolean
            - `ringing` — boolean
          - `smsNumber` — string
    - `total` — number **(required)**
- Errors: `401`, `403`

#### `GET` `/api/v1/Groups`

- operationId: `ListPbxGroups`
- **Response 200** (`ListPbxGroupsResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — ListPbxGroupsResult **(required)**
    - `total` — number **(required)**
    - `records` — array **(required)**
      - _array of_ `PbxGroup`
        - `dn` — string **(required)** — Example: gid=14082460,o=com0,dc=wildix
        - `id` — string **(required)** — Example: 14082460
        - `name` — string **(required)** — Example: Admin
        - `wcgrp` — string
- Errors: `401`, `403`

#### `POST` `/api/v1/pbx/aclgroups`

- operationId: `CreatePbxAclGroup`
- **Request body** (`application/json` — `CreatePbxAclGroupRequestContent`) **(required)**
  - `name` — string **(required)**
  - `inherits` — string
  - `wcgrp` — string
  - `rules` — array **(required)**
    - _array of_ `AclGroupRule`
      - `ability` — string _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
      - `group` — string
      - `rule` — string
- **Response 200** (`CreatePbxAclGroupResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — AclGroup **(required)**
    - `id` — number **(required)**
    - `name` — string **(required)**
    - `dn` — string **(required)**
    - `wcgrp` — string **(required)**
    - `inherits` — string **(required)**
    - `rules` — array **(required)**
      - _array of_ `AclGroupRule`
        - `ability` — string _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
        - `group` — string
        - `rule` — string
    - `adminRules` — string **(required)**
- Errors: `401`, `403`

#### `GET` `/api/v1/pbx/aclgroups/permissions`

- operationId: `GetPbxAclGroupsPermissions`
- **Parameters**
  - `groups[]` (query) — array — User group(s) ID for filter result. Example: ['12345'] or ['12345','67890','134711']
  - `permissions[]` (query) — array — ACL permission(s) key for filter result. Example: ['SEE_CALL_RECORDINGS'] or ['CTI_ANALYTICS','SUPERVISION','SEE_ANALYTICS']
- **Response 200** (`GetPbxAclGroupsPermissionsResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — array **(required)**
    - _array of_ `AclGroupPermission`
      - `ability` — string **(required)** _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
      - `key` — string **(required)**
      - `name` — string **(required)**
      - `containSubGroups` — boolean **(required)**
      - `groups` — array **(required)**
        - _array of_ `AclGroupPermissionItem`
          - `groupDn` — string **(required)**
          - `groupName` — string **(required)**
          - `access` — boolean **(required)**
          - `subGroups` — array **(required)**
            - _array of_ `AclGroupPermissionFlatItem`
              - _(nesting depth limit — see `AclGroupPermissionFlatItem` in the Schemas appendix)_
- Errors: `401`, `403`

#### `DELETE` `/api/v1/pbx/aclgroups/{id}`

- operationId: `DeletePbxAclGroup`
- **Parameters**
  - `id` (path) — number **(required)**
- **Response 200** (`DeletePbxAclGroupResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — string **(required)** _(default=Success)_
- Errors: `401`, `403`

#### `GET` `/api/v1/pbx/settings/callqueues/{groupId}`

Get the settings of a specific Call group on the PBX.

- operationId: `GetCallQueuesSettings`
- **Parameters**
  - `groupId` (path) — number **(required)**
- **Response 200** (`GetCallQueuesSettingsResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — GetCallQueuesSettingsResult **(required)**
    - `id` — number **(required)**
    - `name` — string **(required)**
    - `members` — array **(required)**
      - _array of_ `CallQueuesSettingsMember`
        - `name` — string **(required)**
        - `stateInterface` — string **(required)**
        - `membership` — string **(required)**
        - `penalty` — string **(required)**
        - `callsTaken` — string **(required)**
        - `lastCall` — string **(required)**
        - `isInCall` — string **(required)**
        - `status` — string **(required)**
        - `paused` — string **(required)**
        - `actionID` — string **(required)**
- Errors: `401`, `403`

### Broadcasts

#### `POST` `/api/v1/broadcasts/reload/`

Clear cache for broadcasts

- operationId: `ReloadBroadcasts`
- **Response 200** (`ReloadBroadcastsResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — string **(required)**
- Errors: `401`, `403`

### Pbxes

#### `GET` `/api/v1/network/pbxes/`

Get list of PBXes.

- operationId: `GetPbxes`
- **Response 200** (`GetPbxesResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — GetPbxesResult **(required)**
    - `records` — array **(required)**
      - _array of_ `Pbx`
        - `ip` — string **(required)**
        - `serial` — string **(required)**
        - `host` — string **(required)**
        - `isServer` — boolean **(required)**
        - `port` — number **(required)**
        - `failOver` — string **(required)**
        - `version` — string **(required)**
        - `isUpdateNeeded` — boolean **(required)**
        - `dn` — string **(required)**
- Errors: `401`, `403`

### Notifications

#### `POST` `/api/v1/notifications/`

Notifications

- operationId: `Notifications`
- **Request body** (`application/json` — `NotificationsRequestContent`) **(required)**
  - `from` — string **(required)** — Information about the source of the notification. For example, the name of the camera.
  - `notificationType` — string **(required)** — Type of the alert that is generated.
  - `event` — string **(required)** — Information about the event. What happened.
  - `broadcastMessage` — string **(required)** — The message for announcing into a conference.
  - `broadcastId` — string **(required)** — The broadcast ID to which the message will be sent. _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `playFrequency` — number — How often (each N seconds) a request has to be repeated.
  - `confirmationTimeout` — number — How many seconds the request should wait for the confirmation after the start.
  - `queueTimeout` — number — How many seconds the queued request should wait for starting processing.
  - `origin` — string — Indicates the source of the request.
  - `priority` — number — The priority of the notification.
  - `customRid` — string — The custom request ID.
  - `skipTranscribe` — boolean — Skip notification transcribing.
  - `skills` — array — A list of LDAP department names to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
    - _array of_ `string`
- **Response 200** (`NotificationsResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — NotificationsOutputResult **(required)**
    - `requestId` — string **(required)**
- Errors: `401`, `403`

### Originate

#### `POST` `/api/v1/originate/`

Originate

- operationId: `Originate`
- **Request body** (`application/json` — `OriginateRequestContent`) **(required)**
  - `channel` — string **(required)**
  - `exten` — string
  - `context` — string
  - `priority` — string
  - `application` — string
  - `data` — string
  - `timeout` — string
  - `callerid` — string
  - `variable` — string
  - `account` — string
  - `async` — string
  - `actionid` — string
- **Response 200** (`OriginateResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — string **(required)** _(enum: `Success`)_
- Errors: `401`, `403`

#### `POST` `/api/v1/originate/call/`

Originate call

- operationId: `OriginateCall`
- **Request body** (`application/json` — `OriginateCallRequestContent`) **(required)**
  - `number` — string **(required)** — The phone number.
  - `name` — string — The name
  - `postpone` — string — Date of sending the delayed message. (14/07/2015 15:35)
- **Response 200** (`OriginateCallResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — string **(required)** _(enum: `Success`)_
- Errors: `401`, `403`

### OAuth2

#### `GET` `/api/v1/pbx/applications/oauth2/`

Get the list of all OAuth2 clients on the PBX.

- operationId: `GetPbxOAuth2Clients`
- **Response 200** (`GetPbxOAuth2ClientsResponseContent`)
  - `type` — object **(required)**
  - `result` — GetPbxOAuth2ClientsResult **(required)**
    - `records` — array **(required)**
      - _array of_ `PbxOAuth2ClientListProjection`
        - `id` — string **(required)**
        - `name` — string **(required)**
        - `redirectUri` — array **(required)**
          - _array of_ `string`
        - `secret` — string **(required)**
        - `created` — number **(required)**
        - `expireTime` — number **(required)**
- Errors: `401`, `403`

#### `POST` `/api/v1/pbx/applications/oauth2/`

Create new OAuth2 client in the PBX.

- operationId: `CreatePbxOAuth2Client`
- **Request body** (`application/json` — `CreatePbxOAuth2ClientRequestContent`) **(required)**
  - `name` — string **(required)** — A name of OAuth2 client.
  - `redirectUri` — array **(required)** — Array of redirect URLs, allowed for this client.
    - _array of_ `string`
  - `expireTime` — number **(required)** — Timestamp for expiration of the OAuth2 application. Should not exceed 1 year.
- **Response 200** (`CreatePbxOAuth2ClientResponseContent`)
  - `type` — object **(required)**
  - `result` — PbxOAuth2Client **(required)**
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `redirectUri` — array **(required)**
      - _array of_ `string`
    - `secret` — string **(required)**
    - `created` — number **(required)**
    - `origins` — array **(required)**
      - _array of_ `string`
    - `accessTokenTtl` — number **(required)**
- Errors: `400`, `401`, `403`

#### `PUT` `/api/v1/pbx/applications/oauth2/{id}/`

Update OAuth2 client in the PBX.

- operationId: `UpdatePbxOAuth2Client`
- **Parameters**
  - `id` (path) — string **(required)** — Client ID.
- **Request body** (`application/json` — `UpdatePbxOAuth2ClientRequestContent`) **(required)**
  - `name` — string **(required)** — A name of OAuth2 client.
  - `redirectUri` — array **(required)** — Array of redirect URLs, allowed for this client.
    - _array of_ `string`
- **Response 200** (`UpdatePbxOAuth2ClientResponseContent`)
  - `type` — object **(required)**
  - `result` — PbxOAuth2Client **(required)**
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `redirectUri` — array **(required)**
      - _array of_ `string`
    - `secret` — string **(required)**
    - `created` — number **(required)**
    - `origins` — array **(required)**
      - _array of_ `string`
    - `accessTokenTtl` — number **(required)**
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/api/v1/pbx/applications/oauth2/{id}/`

Update OAuth2 client in the PBX.

- operationId: `DeletePbxOAuth2Client`
- **Parameters**
  - `id` (path) — string **(required)** — Client ID.
- **Response 200** (`DeletePbxOAuth2ClientResponseContent`)
  - `type` — object **(required)**
  - `result` — string **(required)**
- Errors: `401`, `403`, `404`

### User

#### `GET` `/api/v1/personal/info/`

- operationId: `GetPersonalInfo`
- **Parameters**
  - `filter[extension][]` (query) — array
  - `filter[id][]` (query) — array
  - `filter[officePhone][]` (query) — array
  - `filter[mobilePhone][]` (query) — array
  - `filter[name][]` (query) — array
  - `filter[email][]` (query) — array
  - `filter[role][]` (query) — array
  - `filter[dialplan][]` (query) — array
  - `filter[faxDialplan][]` (query) — array
  - `filter[department][]` (query) — array
  - `filter[login][]` (query) — array
  - `filter[groupDn][]` (query) — array
  - `filter[pbxDn][]` (query) — array
  - `filter[licenseType][]` (query) — array
  - `fields` (query) — array
  - `searchFields` (query) — array
  - `search` (query) — string
  - `sort` (query) — array — The field to sort by. The PBX sorts by one field: pass a single item. The list is sent as a repeated parameter and the PBX reads only the last one, so it is deliberately not `@commaDelimited`.
  - `start` (query) — number
  - `count` (query) — number
  - `dir` (query) — string _(enum: `asc`, `desc`)_
  - `searchStrategy` (query) — string _(enum: `contain`, `startsWith`)_
- **Response 200** (`GetPersonalInfoResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — PbxColleague **(required)**
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
- Errors: `401`, `403`

### Call Control

#### `POST` `/api/v2/call-control/answer/`

- operationId: `CallControlAnswer`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlAnswerRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
  - `device` — string — Can specify the device to answer the call on. If not specified, the default device for the user will be used.
- **Response 200** (`CallControlAnswerResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

#### `POST` `/api/v2/call-control/attendant-transfer/`

- operationId: `CallControlAttendantTransfer`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlAttendantTransferRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
  - `destination` — string **(required)** — The destination for a call control operation. This can be a phone number, extension, or another valid identifier. _(pattern=^[0-9a-zA-Z\-\+]+$)_
- **Response 200** (`CallControlAttendantTransferResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

#### `POST` `/api/v2/call-control/blind-transfer/`

- operationId: `CallControlBlindTransfer`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlBlindTransferRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
  - `destination` — string **(required)** — The destination for a call control operation. This can be a phone number, extension, or another valid identifier. _(pattern=^[0-9a-zA-Z\-\+]+$)_
- **Response 200** (`CallControlBlindTransferResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

#### `POST` `/api/v2/call-control/dtmf/`

- operationId: `CallControlDtmf`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlDtmfRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
  - `digits` — string **(required)** — DTMF digits. Allowed characters: 0-9, *, # _(pattern=^[0-9*#]+$)_
- **Response 200** (`CallControlDtmfResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

#### `POST` `/api/v2/call-control/hangup/`

- operationId: `CallControlHangup`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlHangupRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
  - `reason` — string — Optional reason for the hangup. This can provide additional context for the action taken.
- **Response 200** (`CallControlHangupResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

#### `POST` `/api/v2/call-control/hold/`

- operationId: `CallControlHold`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlHoldRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- **Response 200** (`CallControlHoldResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

#### `GET` `/api/v2/call-control/list-calls/`

- operationId: `ListUserActiveCalls`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Response 200** (`ListUserActiveCallsResponseContent`)
  - `calls` — array **(required)**
    - _array of_ `Call`
      - `sipCallId` — string **(required)**
      - `callerNumber` — string **(required)**
      - `callerName` — string
      - `calleeNumber` — string **(required)**
      - `calleeName` — string
      - `state` — string **(required)**
      - `duration` — number **(required)**
- Errors: `401`, `403`

#### `GET` `/api/v2/call-control/list-devices/`

- operationId: `ListUserDevices`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Response 200** (`ListUserDevicesResponseContent`)
  - `devices` — array **(required)**
    - _array of_ `UserDevice`
      - `userAgent` — string **(required)**
      - `contact` — string **(required)**
      - `active` — boolean **(required)**
  - `activeDevice` — UserDevice **(required)**
    - `userAgent` — string **(required)**
    - `contact` — string **(required)**
    - `active` — boolean **(required)**
- Errors: `401`, `403`

#### `POST` `/api/v2/call-control/make-call/`

- operationId: `CallControlMakeCall`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlMakeCallRequestContent`) **(required)**
  - `destination` — string **(required)** — The destination for a call control operation. This can be a phone number, extension, or another valid identifier. _(pattern=^[0-9a-zA-Z\-\+]+$)_
  - `device` — string — Can specify the device to answer the call on. If not specified, the default device for the user will be used.
- **Response 200** (`CallControlMakeCallResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`

#### `POST` `/api/v2/call-control/unhold/`

- operationId: `CallControlUnhold`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlUnholdRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- **Response 200** (`CallControlUnholdResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

#### `POST` `/api/v2/call-control/update-contact-info/`

- operationId: `CallControlUpdateContactInfo`
- **Parameters**
  - `user` (query) — string — Extension, login or email. Only users with root admin authorization can specify a different user. By default, the authorized user will be used. Optional parameter.
- **Request body** (`application/json` — `CallControlUpdateContactInfoRequestContent`) **(required)**
  - `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
  - `name` — string — Contact name
  - `phone` — string — Phone number
- **Response 200** (`CallControlUpdateContactInfoResponseContent`)
  - `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.
- Errors: `401`, `403`, `404`

### Schemas appendix — Cloud PBX Server API

<details><summary>90 component schemas</summary>

**`AclGroup`**

- `id` — number **(required)**
- `name` — string **(required)**
- `dn` — string **(required)**
- `wcgrp` — string **(required)**
- `inherits` — string **(required)**
- `rules` — array **(required)**
  - _array of_ `AclGroupRule`
    - `ability` — string _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
    - `group` — string
    - `rule` — string
- `adminRules` — string **(required)**

**`AclGroupPermission`**

- `ability` — string **(required)** _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
- `key` — string **(required)**
- `name` — string **(required)**
- `containSubGroups` — boolean **(required)**
- `groups` — array **(required)**
  - _array of_ `AclGroupPermissionItem`
    - `groupDn` — string **(required)**
    - `groupName` — string **(required)**
    - `access` — boolean **(required)**
    - `subGroups` — array **(required)**
      - _array of_ `AclGroupPermissionFlatItem`
        - _(nesting depth limit — see `AclGroupPermissionFlatItem` in the Schemas appendix)_

**`AclGroupPermissionAbility`**

- string _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_

**`AclGroupPermissionFlatItem`**

- `groupDn` — string **(required)**
- `groupName` — string **(required)**
- `access` — boolean **(required)**

**`AclGroupPermissionItem`**

- `groupDn` — string **(required)**
- `groupName` — string **(required)**
- `access` — boolean **(required)**
- `subGroups` — array **(required)**
  - _array of_ `AclGroupPermissionFlatItem`
    - `groupDn` — string **(required)**
    - `groupName` — string **(required)**
    - `access` — boolean **(required)**

**`AclGroupRule`**

- `ability` — string _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
- `group` — string
- `rule` — string

**`Call`**

- `sipCallId` — string **(required)**
- `callerNumber` — string **(required)**
- `callerName` — string
- `calleeNumber` — string **(required)**
- `calleeName` — string
- `state` — string **(required)**
- `duration` — number **(required)**

**`CallControlAnswerRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- `device` — string — Can specify the device to answer the call on. If not specified, the default device for the user will be used.

**`CallControlAnswerResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlAttendantTransferRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- `destination` — string **(required)** — The destination for a call control operation. This can be a phone number, extension, or another valid identifier. _(pattern=^[0-9a-zA-Z\-\+]+$)_

**`CallControlAttendantTransferResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlBlindTransferRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- `destination` — string **(required)** — The destination for a call control operation. This can be a phone number, extension, or another valid identifier. _(pattern=^[0-9a-zA-Z\-\+]+$)_

**`CallControlBlindTransferResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlDtmfRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- `digits` — string **(required)** — DTMF digits. Allowed characters: 0-9, *, # _(pattern=^[0-9*#]+$)_

**`CallControlDtmfResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlHangupRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- `reason` — string — Optional reason for the hangup. This can provide additional context for the action taken.

**`CallControlHangupResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlHoldRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_

**`CallControlHoldResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlMakeCallRequestContent`**

- `destination` — string **(required)** — The destination for a call control operation. This can be a phone number, extension, or another valid identifier. _(pattern=^[0-9a-zA-Z\-\+]+$)_
- `device` — string — Can specify the device to answer the call on. If not specified, the default device for the user will be used.

**`CallControlMakeCallResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlUnholdRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_

**`CallControlUnholdResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallControlUpdateContactInfoRequestContent`**

- `sipCallId` — string **(required)** — Call identifier. For makecall action it is not required, for other actions it is required. _(pattern=^[0-9a-zA-Z\-]+$)_
- `name` — string — Contact name
- `phone` — string — Phone number

**`CallControlUpdateContactInfoResponseContent`**

- `message` — string — A message describing the result of the call control operation, providing additional details or error information if applicable.

**`CallQueuesSettingsMember`**

- `name` — string **(required)**
- `stateInterface` — string **(required)**
- `membership` — string **(required)**
- `penalty` — string **(required)**
- `callsTaken` — string **(required)**
- `lastCall` — string **(required)**
- `isInCall` — string **(required)**
- `status` — string **(required)**
- `paused` — string **(required)**
- `actionID` — string **(required)**

**`ChannelNotFoundExceptionResponseContent`**

- `type` — object **(required)**
- `reason` — string **(required)**

**`CreatePbxAclGroupRequestContent`**

- `name` — string **(required)**
- `inherits` — string
- `wcgrp` — string
- `rules` — array **(required)**
  - _array of_ `AclGroupRule`
    - `ability` — string _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
    - `group` — string
    - `rule` — string

**`CreatePbxAclGroupResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — AclGroup **(required)**
  - `id` — number **(required)**
  - `name` — string **(required)**
  - `dn` — string **(required)**
  - `wcgrp` — string **(required)**
  - `inherits` — string **(required)**
  - `rules` — array **(required)**
    - _array of_ `AclGroupRule`
      - `ability` — string _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
      - `group` — string
      - `rule` — string
  - `adminRules` — string **(required)**

**`CreatePbxColleagueRequestContent`**

- `extension` — string **(required)**
- `name` — string **(required)**
- `officePhone` — string
- `mobilePhone` — string
- `faxNumber` — string
- `email` — string
- `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
- `groupDn` — string
- `language` — string
- `dialplan` — string
- `faxDialplan` — string
- `department` — string
- `login` — string
- `password` — string
- `sipPassword` — string
- `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`CreatePbxColleagueResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — PbxColleague **(required)**
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

**`CreatePbxOAuth2ClientRequestContent`**

- `name` — string **(required)** — A name of OAuth2 client.
- `redirectUri` — array **(required)** — Array of redirect URLs, allowed for this client.
  - _array of_ `string`
- `expireTime` — number **(required)** — Timestamp for expiration of the OAuth2 application. Should not exceed 1 year.

**`CreatePbxOAuth2ClientResponseContent`**

- `type` — object **(required)**
- `result` — PbxOAuth2Client **(required)**
  - `id` — string **(required)**
  - `name` — string **(required)**
  - `redirectUri` — array **(required)**
    - _array of_ `string`
  - `secret` — string **(required)**
  - `created` — number **(required)**
  - `origins` — array **(required)**
    - _array of_ `string`
  - `accessTokenTtl` — number **(required)**

**`DeletePbxAclGroupResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — string **(required)** _(default=Success)_

**`DeletePbxColleagueResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — string **(required)** _(default=Success)_

**`DeletePbxOAuth2ClientResponseContent`**

- `type` — object **(required)**
- `result` — string **(required)**

**`GetCallQueuesSettingsResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — GetCallQueuesSettingsResult **(required)**
  - `id` — number **(required)**
  - `name` — string **(required)**
  - `members` — array **(required)**
    - _array of_ `CallQueuesSettingsMember`
      - `name` — string **(required)**
      - `stateInterface` — string **(required)**
      - `membership` — string **(required)**
      - `penalty` — string **(required)**
      - `callsTaken` — string **(required)**
      - `lastCall` — string **(required)**
      - `isInCall` — string **(required)**
      - `status` — string **(required)**
      - `paused` — string **(required)**
      - `actionID` — string **(required)**

**`GetCallQueuesSettingsResult`**

- `id` — number **(required)**
- `name` — string **(required)**
- `members` — array **(required)**
  - _array of_ `CallQueuesSettingsMember`
    - `name` — string **(required)**
    - `stateInterface` — string **(required)**
    - `membership` — string **(required)**
    - `penalty` — string **(required)**
    - `callsTaken` — string **(required)**
    - `lastCall` — string **(required)**
    - `isInCall` — string **(required)**
    - `status` — string **(required)**
    - `paused` — string **(required)**
    - `actionID` — string **(required)**

**`GetColleagueByIdResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — PbxColleague **(required)**
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

**`GetDepartmentsResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — GetDepartmentsResult **(required)**
  - `records` — array **(required)**
    - _array of_ `PbxDepartment`
      - `id` — string **(required)** — Department id.
      - `name` — string **(required)** — Department name.
      - `users` — array — User extensions in this department.
        - _array of_ `string`
      - `items` — array — Child departments (recursive).
        - _(nesting depth limit — see `PbxDepartment` in the Schemas appendix)_

**`GetDepartmentsResult`**

- `records` — array **(required)**
  - _array of_ `PbxDepartment`
    - `id` — string **(required)** — Department id.
    - `name` — string **(required)** — Department name.
    - `users` — array — User extensions in this department.
      - _array of_ `string`
    - `items` — array — Child departments (recursive).
      - _array of_ `PbxDepartment`
        - _(nesting depth limit — see `PbxDepartment` in the Schemas appendix)_

**`GetPbxAclGroupsPermissionsResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — array **(required)**
  - _array of_ `AclGroupPermission`
    - `ability` — string **(required)** _(enum: `use`, `nouse`, `can`, `cannot`, `yes`, `no`)_
    - `key` — string **(required)**
    - `name` — string **(required)**
    - `containSubGroups` — boolean **(required)**
    - `groups` — array **(required)**
      - _array of_ `AclGroupPermissionItem`
        - _(nesting depth limit — see `AclGroupPermissionItem` in the Schemas appendix)_

**`GetPbxCallGroupsResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — GetPbxCallGroupsResult **(required)**
  - `records` — array **(required)**
    - _array of_ `PbxCallGroup`
      - `id` — number **(required)**
      - `title` — string **(required)**
      - `members` — array **(required)**
        - _array of_ `string`
      - `settings` — PbxCallGroupSettings **(required)**
        - _(nesting depth limit — see `PbxCallGroupSettings` in the Schemas appendix)_
  - `total` — number **(required)**

**`GetPbxCallGroupsResult`**

- `records` — array **(required)**
  - _array of_ `PbxCallGroup`
    - `id` — number **(required)**
    - `title` — string **(required)**
    - `members` — array **(required)**
      - _array of_ `string`
    - `settings` — PbxCallGroupSettings **(required)**
      - `queueManager` — string
      - `cid` — string
      - `autoPause` — string
      - `autoPauseTime` — number
      - `autoPauseDelay` — number
      - `autoPauseBusy` — boolean
      - `autoPauseUnAvail` — boolean
      - `maxLen` — number
      - `retry` — number
      - `ringInUse` — boolean
      - `strategy` — string
      - `defaultPriority` — number
      - `timeout` — number
      - `weight` — number
      - `wrapUpTime` — number
      - `rule` — string
      - `announce` — PbxCallGroupAnnounce
        - _(nesting depth limit — see `PbxCallGroupAnnounce` in the Schemas appendix)_
      - `exitAllMembers` — PbxCallGroupExitAllMembers
        - _(nesting depth limit — see `PbxCallGroupExitAllMembers` in the Schemas appendix)_
      - `smsNumber` — string
- `total` — number **(required)**

**`GetPbxColleaguesDir`**

- string _(enum: `asc`, `desc`)_

**`GetPbxColleaguesResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — GetPbxColleaguesResult **(required)**
  - `records` — array **(required)**
    - _array of_ `PbxColleague`
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
  - `total` — number **(required)**

**`GetPbxColleaguesResult`**

- `records` — array **(required)**
  - _array of_ `PbxColleague`
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
- `total` — number **(required)**

**`GetPbxOAuth2ClientsResponseContent`**

- `type` — object **(required)**
- `result` — GetPbxOAuth2ClientsResult **(required)**
  - `records` — array **(required)**
    - _array of_ `PbxOAuth2ClientListProjection`
      - `id` — string **(required)**
      - `name` — string **(required)**
      - `redirectUri` — array **(required)**
        - _array of_ `string`
      - `secret` — string **(required)**
      - `created` — number **(required)**
      - `expireTime` — number **(required)**

**`GetPbxOAuth2ClientsResult`**

- `records` — array **(required)**
  - _array of_ `PbxOAuth2ClientListProjection`
    - `id` — string **(required)**
    - `name` — string **(required)**
    - `redirectUri` — array **(required)**
      - _array of_ `string`
    - `secret` — string **(required)**
    - `created` — number **(required)**
    - `expireTime` — number **(required)**

**`GetPbxesResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — GetPbxesResult **(required)**
  - `records` — array **(required)**
    - _array of_ `Pbx`
      - `ip` — string **(required)**
      - `serial` — string **(required)**
      - `host` — string **(required)**
      - `isServer` — boolean **(required)**
      - `port` — number **(required)**
      - `failOver` — string **(required)**
      - `version` — string **(required)**
      - `isUpdateNeeded` — boolean **(required)**
      - `dn` — string **(required)**

**`GetPbxesResult`**

- `records` — array **(required)**
  - _array of_ `Pbx`
    - `ip` — string **(required)**
    - `serial` — string **(required)**
    - `host` — string **(required)**
    - `isServer` — boolean **(required)**
    - `port` — number **(required)**
    - `failOver` — string **(required)**
    - `version` — string **(required)**
    - `isUpdateNeeded` — boolean **(required)**
    - `dn` — string **(required)**

**`GetPersonalInfoResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — PbxColleague **(required)**
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

**`ListPbxGroupsResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — ListPbxGroupsResult **(required)**
  - `total` — number **(required)**
  - `records` — array **(required)**
    - _array of_ `PbxGroup`
      - `dn` — string **(required)** — Example: gid=14082460,o=com0,dc=wildix
      - `id` — string **(required)** — Example: 14082460
      - `name` — string **(required)** — Example: Admin
      - `wcgrp` — string

**`ListPbxGroupsResult`**

- `total` — number **(required)**
- `records` — array **(required)**
  - _array of_ `PbxGroup`
    - `dn` — string **(required)** — Example: gid=14082460,o=com0,dc=wildix
    - `id` — string **(required)** — Example: 14082460
    - `name` — string **(required)** — Example: Admin
    - `wcgrp` — string

**`ListUserActiveCallsResponseContent`**

- `calls` — array **(required)**
  - _array of_ `Call`
    - `sipCallId` — string **(required)**
    - `callerNumber` — string **(required)**
    - `callerName` — string
    - `calleeNumber` — string **(required)**
    - `calleeName` — string
    - `state` — string **(required)**
    - `duration` — number **(required)**

**`ListUserDevicesResponseContent`**

- `devices` — array **(required)**
  - _array of_ `UserDevice`
    - `userAgent` — string **(required)**
    - `contact` — string **(required)**
    - `active` — boolean **(required)**
- `activeDevice` — UserDevice **(required)**
  - `userAgent` — string **(required)**
  - `contact` — string **(required)**
  - `active` — boolean **(required)**

**`NotificationsOutputResult`**

- `requestId` — string **(required)**

**`NotificationsRequestContent`**

- `from` — string **(required)** — Information about the source of the notification. For example, the name of the camera.
- `notificationType` — string **(required)** — Type of the alert that is generated.
- `event` — string **(required)** — Information about the event. What happened.
- `broadcastMessage` — string **(required)** — The message for announcing into a conference.
- `broadcastId` — string **(required)** — The broadcast ID to which the message will be sent. _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
- `playFrequency` — number — How often (each N seconds) a request has to be repeated.
- `confirmationTimeout` — number — How many seconds the request should wait for the confirmation after the start.
- `queueTimeout` — number — How many seconds the queued request should wait for starting processing.
- `origin` — string — Indicates the source of the request.
- `priority` — number — The priority of the notification.
- `customRid` — string — The custom request ID.
- `skipTranscribe` — boolean — Skip notification transcribing.
- `skills` — array — A list of LDAP department names to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
  - _array of_ `string`

**`NotificationsResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — NotificationsOutputResult **(required)**
  - `requestId` — string **(required)**

**`OriginateCallRequestContent`**

- `number` — string **(required)** — The phone number.
- `name` — string — The name
- `postpone` — string — Date of sending the delayed message. (14/07/2015 15:35)

**`OriginateCallResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — string **(required)** _(enum: `Success`)_

**`OriginateRequestContent`**

- `channel` — string **(required)**
- `exten` — string
- `context` — string
- `priority` — string
- `application` — string
- `data` — string
- `timeout` — string
- `callerid` — string
- `variable` — string
- `account` — string
- `async` — string
- `actionid` — string

**`OriginateResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — string **(required)** _(enum: `Success`)_

**`Pbx`**

- `ip` — string **(required)**
- `serial` — string **(required)**
- `host` — string **(required)**
- `isServer` — boolean **(required)**
- `port` — number **(required)**
- `failOver` — string **(required)**
- `version` — string **(required)**
- `isUpdateNeeded` — boolean **(required)**
- `dn` — string **(required)**

**`PbxCallGroup`**

- `id` — number **(required)**
- `title` — string **(required)**
- `members` — array **(required)**
  - _array of_ `string`
- `settings` — PbxCallGroupSettings **(required)**
  - `queueManager` — string
  - `cid` — string
  - `autoPause` — string
  - `autoPauseTime` — number
  - `autoPauseDelay` — number
  - `autoPauseBusy` — boolean
  - `autoPauseUnAvail` — boolean
  - `maxLen` — number
  - `retry` — number
  - `ringInUse` — boolean
  - `strategy` — string
  - `defaultPriority` — number
  - `timeout` — number
  - `weight` — number
  - `wrapUpTime` — number
  - `rule` — string
  - `announce` — PbxCallGroupAnnounce
    - `frequency` — number
    - `holdTime` — string
    - `roundSeconds` — number
  - `exitAllMembers` — PbxCallGroupExitAllMembers
    - `busy` — boolean
    - `paused` — boolean
    - `ringing` — boolean
  - `smsNumber` — string

**`PbxCallGroupAnnounce`**

- `frequency` — number
- `holdTime` — string
- `roundSeconds` — number

**`PbxCallGroupExitAllMembers`**

- `busy` — boolean
- `paused` — boolean
- `ringing` — boolean

**`PbxCallGroupSettings`**

- `queueManager` — string
- `cid` — string
- `autoPause` — string
- `autoPauseTime` — number
- `autoPauseDelay` — number
- `autoPauseBusy` — boolean
- `autoPauseUnAvail` — boolean
- `maxLen` — number
- `retry` — number
- `ringInUse` — boolean
- `strategy` — string
- `defaultPriority` — number
- `timeout` — number
- `weight` — number
- `wrapUpTime` — number
- `rule` — string
- `announce` — PbxCallGroupAnnounce
  - `frequency` — number
  - `holdTime` — string
  - `roundSeconds` — number
- `exitAllMembers` — PbxCallGroupExitAllMembers
  - `busy` — boolean
  - `paused` — boolean
  - `ringing` — boolean
- `smsNumber` — string

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

**`PbxDepartment`**

- `id` — string **(required)** — Department id.
- `name` — string **(required)** — Department name.
- `users` — array — User extensions in this department.
  - _array of_ `string`
- `items` — array — Child departments (recursive).
  - _array of_ `PbxDepartment`
    - _(nesting depth limit — see `PbxDepartment` in the Schemas appendix)_

**`PbxGroup`**

- `dn` — string **(required)** — Example: gid=14082460,o=com0,dc=wildix
- `id` — string **(required)** — Example: 14082460
- `name` — string **(required)** — Example: Admin
- `wcgrp` — string

**`PbxLicenseType`**

- string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_

**`PbxOAuth2Client`**

- `id` — string **(required)**
- `name` — string **(required)**
- `redirectUri` — array **(required)**
  - _array of_ `string`
- `secret` — string **(required)**
- `created` — number **(required)**
- `origins` — array **(required)**
  - _array of_ `string`
- `accessTokenTtl` — number **(required)**

**`PbxOAuth2ClientListProjection`**

- `id` — string **(required)**
- `name` — string **(required)**
- `redirectUri` — array **(required)**
  - _array of_ `string`
- `secret` — string **(required)**
- `created` — number **(required)**
- `expireTime` — number **(required)**

**`ReloadBroadcastsResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — string **(required)**

**`ResponseResult`**

- string _(enum: `Success`)_

**`ResponseType`**

- string _(enum: `result`, `error`)_

**`UpdatePbxColleagueRequestContent`**

- `extension` — string
- `name` — string
- `officePhone` — string
- `mobilePhone` — string
- `faxNumber` — string
- `email` — string
- `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
- `groupDn` — string
- `language` — string
- `dialplan` — string
- `faxDialplan` — string
- `department` — string
- `login` — string
- `password` — string
- `sipPassword` — string
- `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- `picture` — string

**`UpdatePbxColleagueResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — PbxColleague **(required)**
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

**`UpdatePbxOAuth2ClientRequestContent`**

- `name` — string **(required)** — A name of OAuth2 client.
- `redirectUri` — array **(required)** — Array of redirect URLs, allowed for this client.
  - _array of_ `string`

**`UpdatePbxOAuth2ClientResponseContent`**

- `type` — object **(required)**
- `result` — PbxOAuth2Client **(required)**
  - `id` — string **(required)**
  - `name` — string **(required)**
  - `redirectUri` — array **(required)**
    - _array of_ `string`
  - `secret` — string **(required)**
  - `created` — number **(required)**
  - `origins` — array **(required)**
    - _array of_ `string`
  - `accessTokenTtl` — number **(required)**

**`UserDevice`**

- `userAgent` — string **(required)**
- `contact` — string **(required)**
- `active` — boolean **(required)**

**`WmsErrorItem`**

- `field` — string **(required)**
- `reason` — string **(required)**

**`WmsForbiddenExceptionResponseContent`**

- `type` — object **(required)**
- `reason` — string **(required)**

**`WmsNotFoundExceptionResponseContent`**

- `type` — object **(required)**
- `reason` — string **(required)**

**`WmsUnauthorizedExceptionResponseContent`**

- `type` — object **(required)**
- `reason` — string **(required)**

**`WmsValidationExceptionResponseContent`**

- `type` — object **(required)**
- `reason` — string **(required)**
- `errors` — array **(required)**
  - _array of_ `WmsErrorItem`
    - `field` — string **(required)**
    - `reason` — string **(required)**

</details>
