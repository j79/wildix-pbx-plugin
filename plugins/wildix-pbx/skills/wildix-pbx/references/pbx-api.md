## PBX API

_OpenAPI: Wildix WMS Interface API — version 1.0_

**Servers**

- `https://{subdomain}.wildixin.com:{port}/api/v1` — 

### Colleagues

#### `GET` `/Colleagues/`

**Get colleagues**

Get a filtered list of PBX users by certain criteria

- operationId: `getColleagues`
- **Scopes**: `colleagues:read`, `pbx:read`
- **Company API Key scope**: `colleagues:read`
- **Parameters**
  - `filter` (query) — array
  - `fields` (query) — string — Fields (comma-separated) _(enum: `extension`, `officePhone`, `mobilePhone`, `faxNumber`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, … (+9))_
  - `searchFields` (query) — string — Search fields (comma-separated) _(enum: `extension`, `officePhone`, `mobilePhone`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, `login`, … (+6))_
  - `search` (query) — string — A string for search or array of strings (logical OR).
  - `sort` (query) — string — The name of a field by which the result should be sorted. _(enum: `extension`, `officePhone`, `mobilePhone`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, `login`, … (+4))_
  - `dir` (query) — string — Sorting direction. _(enum: `asc`, `desc`)_
  - `count` (query) — integer — Maximum number of characters in the result output.
  - `start` (query) — integer — The result offset.
  - `searchStrategy` (query) — string — Search strategy. Search for data which contains or starts with the inquired characters. *Wildcard search doesn't work with fields groupDn and pbxDn.* _(default=contain; enum: `contain`, `startsWith`)_
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `Colleague`
        - `id` — string
        - `dn` — string _(minLen=4)_
        - `pbxDn` — string _(minLen=4)_
        - `jid` — string _(format=email)_
        - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
        - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
        - `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
        - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
        - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
        - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
        - `email` — string _(format=email)_
        - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
        - `groupDn` — string _(minLen=4)_
        - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
        - `dialplan` — string
        - `faxDialplan` — string
        - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
        - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
        - `picture` — string
        - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
        - `groupName` — string — Group name
    - `total` — integer
  - `type` — string _(format=result)_
- Errors: `400`, `401`, `403`

#### `GET` `/Colleagues/{id}/`

**Get colleague**

Get filtered data of a PBX user

- operationId: `getColleague`
- **Scopes**: `colleagues:read`, `pbx:read`
- **Company API Key scope**: `colleagues:read`
- **Parameters**
  - `id` (path) — integer **(required)**
  - `fields` (query) — string — Search fields (comma-separated). _(enum: `extension`, `officePhone`, `mobilePhone`, `faxNumber`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, … (+9))_
- **Response 200** (`ApiResponseColleague`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `id` — string
    - `dn` — string _(minLen=4)_
    - `pbxDn` — string _(minLen=4)_
    - `jid` — string _(format=email)_
    - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
    - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
    - `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `email` — string _(format=email)_
    - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
    - `groupDn` — string _(minLen=4)_
    - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
    - `dialplan` — string
    - `faxDialplan` — string
    - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
    - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `picture` — string
    - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
    - `groupName` — string — Group name
- Errors: `401`, `403`, `404`

#### `GET` `/PBX/Colleagues/`

**Get colleagues (with ACL)**

Get a filtered list of PBX users by certain criteria.
****Available only for administrators with enabled ACL permissions to manage groups****

- operationId: `getPBXColleagues`
- **Scopes**: `colleagues:read`, `pbx:read`
- **Company API Key scope**: `colleagues:read`
- **Parameters**
  - `filter` (query) — array
  - `fields` (query) — string — Fields (comma-separated) _(enum: `extension`, `officePhone`, `mobilePhone`, `faxNumber`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, … (+9))_
  - `searchFields` (query) — string — Search fields (comma-separated) _(enum: `extension`, `officePhone`, `mobilePhone`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, `login`, … (+5))_
  - `search` (query) — string — A string for search or array of strings (logical OR).
  - `sort` (query) — string — The name of a field by which the result should be sorted. _(enum: `extension`, `officePhone`, `mobilePhone`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, `login`, … (+4))_
  - `dir` (query) — string — Sorting direction. _(enum: `asc`, `desc`)_
  - `count` (query) — integer — Maximum number of characters in the result output.
  - `start` (query) — integer — The result offset.
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `Colleague`
        - `id` — string
        - `dn` — string _(minLen=4)_
        - `pbxDn` — string _(minLen=4)_
        - `jid` — string _(format=email)_
        - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
        - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
        - `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
        - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
        - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
        - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
        - `email` — string _(format=email)_
        - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
        - `groupDn` — string _(minLen=4)_
        - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
        - `dialplan` — string
        - `faxDialplan` — string
        - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
        - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
        - `picture` — string
        - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
        - `groupName` — string — Group name
    - `total` — integer
  - `type` — string _(format=result)_
- Errors: `401`, `403`

#### `POST` `/PBX/Colleagues/`

**Create colleague (with ACL)**

Create a new user on the PBX.
****Available only for administrators with enabled ACL permissions to manage groups****

- operationId: `addPBXColleague`
- **Scopes**: `colleagues:*`, `pbx:*`
- **Company API Key scope**: `colleagues:*`
- **Request body** (`application/json`) **(required)**
  - `extension` — string **(required)** — A numeric string _(minLen=2; maxLen=50)_
  - `name` — string **(required)** — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
  - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `email` — string — Valid email. Needed for the proper functioning of the notification features _(format=email)_
  - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
  - `groupDn` — string _(minLen=4)_
  - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
  - `dialplan` — string
  - `faxDialplan` — string
  - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
  - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
  - `password` — string — Password must consist of at least 8 symbols and contain at least one special character (!@*+=><;), digit (0-9), uppercase (A-Z) and lowercase (a-z) letter. _(minLen=8)_
  - `sipPassword` — string — Password must consist of at least 10 symbols and contain at least one special character (%!@#*), digit (0-9), uppercase (A-Z) and lowercase (a-z) letter. _(minLen=10)_
  - `licenseType` — string **(required)** _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- **Response 200** (`ApiResponseColleague`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `id` — string
    - `dn` — string _(minLen=4)_
    - `pbxDn` — string _(minLen=4)_
    - `jid` — string _(format=email)_
    - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
    - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
    - `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `email` — string _(format=email)_
    - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
    - `groupDn` — string _(minLen=4)_
    - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
    - `dialplan` — string
    - `faxDialplan` — string
    - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
    - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `picture` — string
    - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
    - `groupName` — string — Group name
- Errors: `400`, `401`, `403`

#### `GET` `/PBX/Colleagues/{id}/`

**Get colleague (with ACL)**

Get filtered data of a PBX user
****Available only for administrators with enabled ACL permissions to manage groups****

- operationId: `getPBXColleague`
- **Scopes**: `colleagues:read`, `pbx:read`
- **Company API Key scope**: `colleagues:read`
- **Parameters**
  - `id` (path) — integer **(required)**
  - `fields` (query) — string — Fields (comma-separated) _(enum: `extension`, `officePhone`, `mobilePhone`, `faxNumber`, `name`, `email`, `role`, `groupDn`, `language`, `dialplan`, `faxDialplan`, `department`, … (+9))_
- **Response 200** (`ApiResponseColleague`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `id` — string
    - `dn` — string _(minLen=4)_
    - `pbxDn` — string _(minLen=4)_
    - `jid` — string _(format=email)_
    - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
    - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
    - `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `email` — string _(format=email)_
    - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
    - `groupDn` — string _(minLen=4)_
    - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
    - `dialplan` — string
    - `faxDialplan` — string
    - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
    - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `picture` — string
    - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
    - `groupName` — string — Group name
- Errors: `401`, `403`, `404`

#### `PUT` `/PBX/Colleagues/{id}/`

**Update colleague (with ACL)**

Update some data of a user on the PBX
****Available only for administrators with enabled ACL permissions to manage groups****

- operationId: `updatePBXColleague`
- **Scopes**: `colleagues:*`, `pbx:*`
- **Company API Key scope**: `colleagues:*`
- **Parameters**
  - `id` (path) — integer **(required)**
  - `transferRnaChats` (query) — boolean — If true transfer Collaboration 7/x-bees/x-hoppers chats to the new email
- **Request body** (`application/json`)
  - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
  - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
  - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `email` — string _(format=email)_
  - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
  - `groupDn` — string _(minLen=4)_
  - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
  - `dialplan` — string
  - `faxDialplan` — string
  - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
  - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
  - `password` — string — Password must consist of at least 8 symbols and contain at least one special character (!@*+=><;), digit (0-9), uppercase (A-Z) and lowercase (a-z) letter. _(minLen=8)_
  - `sipPassword` — string — Password must consist of at least 10 symbols and contain at least one special character (%!@#*), digit (0-9), uppercase (A-Z) and lowercase (a-z) letter. _(minLen=10)_
  - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- **Response 200** (`ApiResponseColleague`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `id` — string
    - `dn` — string _(minLen=4)_
    - `pbxDn` — string _(minLen=4)_
    - `jid` — string _(format=email)_
    - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
    - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
    - `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
    - `email` — string _(format=email)_
    - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
    - `groupDn` — string _(minLen=4)_
    - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
    - `dialplan` — string
    - `faxDialplan` — string
    - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
    - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
    - `picture` — string
    - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
    - `groupName` — string — Group name
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/PBX/Colleagues/{id}/`

**Delete colleague (with ACL)**

Delete a user from the PBX
****Available only for administrators with enabled ACL permissions to manage groups****

- operationId: `deletePBXColleague`
- **Scopes**: `colleagues:*`, `pbx:*`
- **Company API Key scope**: `colleagues:*`
- **Parameters**
  - `id` (path) — integer **(required)**
  - `data[]` (query) — array — Array of options for deletion.
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `403`, `404`

#### `PUT` `/PBX/presence/`

**Set batch presence for colleagues**

Set batch presence for colleagues
****Available only for administrators****

- operationId: `setBatchPresence`
- **Scopes**: `colleagues:*`, `pbx:*`
- **Company API Key scope**: `colleagues:*`
- **Request body** (`application/json`)
  - `items` — array — Presences items
    - _array of_ `object`
      - `extension` — string **(required)** — Colleague extension
      - `status` — string **(required)** — Status _(enum: `available`, `away`, `dnd`, `mur`)_
      - `message` — string — Status message _(default=empty)_
      - `until` — string — Format: "19/09/2017 11:30" in UTC _(default=empty)_
- **Response 200**
  - `type` — string **(required)** _(enum: `result`, `warning`)_
  - `result` — string **(required)** _(enum: `Success`)_
  - `reason` — string — Warning reason
  - `warnings` — object — Information about failed changes (Extension => Error reason)
- Errors: `401`, `403`

#### `PUT` `/PBX/Colleagues/{id}/preferences/`

**Copy preferences from user**

Copy preferences from user
****Available only for administrators****

- operationId: `preferences`
- **Scopes**: `colleagues:*`, `pbx:*`
- **Company API Key scope**: `colleagues:*`
- **Parameters**
  - `id` (path) — integer **(required)**
- **Request body** (`application/json`)
  - `from` — string — UID from whom preferences should be copied
- **Response 200**
  - `type` — string **(required)** _(enum: `result`, `warning`)_
  - `result` — string **(required)** _(enum: `Success`)_
  - `reason` — string — Warning reason
  - `warnings` — object — Information about failed changes (Extension => Error reason)
- Errors: `401`, `403`, `404`

### Applications SimpleToken

#### `GET` `/PBX/Applications/SimpleToken/`

**Get simple token applications list**

Returns the list of all simple token applications.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplicationsSimple`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — string — Application ID
        - `name` — string — Application name
        - `secret` — string — Secret key
        - `pbxUser` — string — PBX user (login or extension)
        - `created` — integer — Application created timestamp
        - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/PBX/Applications/SimpleToken/`

**Add new application**

Adds a new simple token application.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplicationsSimpleCreate`
- **Request body** (`application/json`)
  - `name` — string — Application name (required)
  - `pbxUser` — string — PBX user, login or extension (required)
  - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
- **Response 200**
  - `result` — ApplicationItem3
    - `id` — string — Application ID
    - `name` — string — Application name
    - `secret` — string — Secret key
    - `pbxUser` — string — PBX user (login or extension)
    - `created` — integer — Application created timestamp
    - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/PBX/Applications/SimpleToken/{id}/`

**Update application**

Updates simple token application settings.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplicationsSimpleUpdate`
- **Parameters**
  - `id` (path) — string **(required)** — Application ID
- **Request body** (`application/json`)
  - `name` — string — Application name (required)
  - `pbxUser` — string — PBX user, login or extension (required)
  - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
- **Response 200**
  - `result` — ApplicationItem3
    - `id` — string — Application ID
    - `name` — string — Application name
    - `secret` — string — Secret key
    - `pbxUser` — string — PBX user (login or extension)
    - `created` — integer — Application created timestamp
    - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/PBX/Applications/SimpleToken/{id}/`

**Delete application**

Deletes simple token application settings.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplicationsSimpleDelete`
- **Parameters**
  - `id` (path) — string **(required)** — Application ID
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Applications S2S

#### `GET` `/PBX/Applications/s2s/`

**Get applications list**

Returns the list of all customers applications.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplications`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — string — Application ID
        - `app` — string — Application name
        - `secret` — string — Secret key
        - `pbxUser` — string — PBX user (login or extension)
        - `created` — integer — Application created timestamp
        - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/PBX/Applications/s2s/`

**Add a new application**

Adds a new customers application.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplicationsCreate`
- **Request body** (`application/json`)
  - `app` — string — Application name (required)
  - `pbxUser` — string — PBX user, login or extension (required)
  - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
- **Response 200**
  - `result` — ApplicationItem
    - `id` — string — Application ID
    - `app` — string — Application name
    - `secret` — string — Secret key
    - `pbxUser` — string — PBX user (login or extension)
    - `created` — integer — Application created timestamp
    - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/PBX/Applications/s2s/{id}/`

**Update application.**

Update customers application settings.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplicationsUpdate`
- **Request body** (`application/json`)
  - `app` — string — Application name (required)
  - `pbxUser` — string — PBX user, login or extension (required)
  - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
- **Response 200**
  - `result` — ApplicationItem
    - `id` — string — Application ID
    - `app` — string — Application name
    - `secret` — string — Secret key
    - `pbxUser` — string — PBX user (login or extension)
    - `created` — integer — Application created timestamp
    - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/PBX/Applications/s2s/{id}/`

**Delete application**

Deletes customers application settings.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxApplicationsDelete`
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Applications OAuth2

#### `GET` `/PBX/Applications/OAuth2/`

**Get OAuth2.0 applications list**

Returns the list of OAuth2.0 applications.

- operationId: `oauth2Applications`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — string — Application ID
        - `name` — string — Application name
        - `secret` — string — Secret key
        - `accessTokenTtl` — integer — Lifetime of the access token
        - `created` — integer — Application created timestamp
        - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
        - `redirectUri` — array — List of redirect URIs
          - _array of_ `any`
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/PBX/Applications/OAuth2/`

**Add a new OAuth2.0 application.**

Add a new OAuth2.0 application.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `oauth2ApplicationsCreate`
- **Request body** (`application/json`)
  - `name` — string — Application name (required)
  - `accessTokenTtl` — integer — Lifetime of the access token, in minutes (required) _(default=10; enum: `1`, `10`, `30`, `60`, `180`, `360`, `720`, `1440`, `4320`, `10080`, `20160`, `40320`)_
  - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `redirectUri` — Array — List of redirect URIs
- **Response 200**
  - `result` — ApplicationItem2
    - `id` — string — Application ID
    - `name` — string — Application name
    - `secret` — string — Secret key
    - `accessTokenTtl` — integer — Lifetime of the access token
    - `created` — integer — Application created timestamp
    - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
    - `redirectUri` — array — List of redirect URIs
      - _array of_ `any`
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/PBX/Applications/OAuth2/{id}/`

**Update OAuth2.0 application**

Update OAuth2.0 application settings.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `oauth2ApplicationsUpdate`
- **Request body** (`application/json`)
  - `name` — string — Application name
  - `accessTokenTtl` — integer — Lifetime of the access token, in minutes _(default=10; enum: `1`, `10`, `30`, `60`, `180`, `360`, `720`, `1440`, `4320`, `10080`, `20160`, `40320`)_
  - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
  - `redirectUri` — array of strings — List of redirect URIs
- **Response 200**
  - `result` — ApplicationItem2
    - `id` — string — Application ID
    - `name` — string — Application name
    - `secret` — string — Secret key
    - `accessTokenTtl` — integer — Lifetime of the access token
    - `created` — integer — Application created timestamp
    - `expireTime` — integer — Token expiration timestamp (Unix timestamp)
    - `redirectUri` — array — List of redirect URIs
      - _array of_ `any`
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/PBX/Applications/OAuth2/{id}/`

**Delete OAuth2.0 application**

Delete OAuth2.0 application settings.
<p style="color:red">Available only for user admin (root)</p>

- operationId: `oauth2ApplicationsDelete`
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### PBX

#### `GET` `/PBX/Users/Sip/Registrations`

**Get SIP proxy registrations for all users**

Returns SIP proxy registrations for all users

- operationId: `getSipRegistrationsForAllUsers`
- **Response 200** (`ApiResponseSipRegistrations`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
- Errors: `401`, `403`

#### `GET` `/PBX/Users/{extensions}/Sip/Registrations`

**Get SIP proxy registrations by users extensions**

Returns SIP proxy registrations for given user extensions

- operationId: `getSipRegistrationsByUsersExtensions`
- **Parameters**
  - `extensions` (path) — string **(required)** — User extensions separated by commas
- **Response 200** (`ApiResponseSipRegistrations`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
- Errors: `401`, `403`

#### `GET` `/PBX/AclGroups/`

**Get all ACL groups managed by the user**

This endpoint is available only to users who can manage ACL groups

- operationId: `getPBXAclGroups`
- **Scopes**: `aclgroups:read`, `pbx:read`
- **Company API Key scope**: `aclgroups:read`
- **Parameters**
  - `fields` (query) — string — Fields (comma-separated)
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `records` — array
      - _array of_ `object`
        - `dn` — string
        - `id` — string — A numeric string
        - `name` — string
        - `wcgrp` — string — A numeric string
        - `inherits` — object
          - `dn` — string **(required)**
          - `name` — string
        - `rules` — array
          - _array of_ `object`
            - `rule` — string **(required)**
            - `ability` — string **(required)** _(enum: `True`, `False`, `set`, `noset`, `use`, `nouse`, `call`, `nocall`)_
            - `group` — string **(required)**
        - `adminRules` — array
          - _array of_ `object`
            - `subject` — string **(required)**
            - `operation` — string **(required)** _(enum: `epbx`, `noepbx`, `egroup`, `noegroup`, `epage`, `noepage`, `eperm`, `noeperm`)_
- Errors: `401`, `403`, `500`

#### `POST` `/PBX/AclGroups/`

**Add a new ACL group**

This endpoint is available only to the user who has "admin" username

- operationId: `addPBXAclGroup`
- **Scopes**: `aclgroups:*`, `pbx:*`
- **Company API Key scope**: `aclgroups:*`
- **Request body** (`application/json`)
  - `name` — string **(required)**
  - `wcgrp` — string — A numeric string.
  - `inherits[dn]` — string — A DN of a parent group.
  - `rules[<index>][rule]` — string — A rule from the list of available rules.
  - `rules[<index>][ability]` — string _(enum: `True`, `False`, `set`, `noset`, `use`, `nouse`, `call`, `nocall`)_
  - `rules[<index>][group]` — string — A group DN to which this rule applies.
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `dn` — string
    - `id` — string — A numeric string
    - `name` — string
    - `wcgrp` — string — A numeric string
    - `inherits` — object
      - `dn` — string **(required)**
      - `name` — string
    - `rules` — array
      - _array of_ `object`
        - `rule` — string **(required)**
        - `ability` — string **(required)** _(enum: `True`, `False`, `set`, `noset`, `use`, `nouse`, `call`, `nocall`)_
        - `group` — string **(required)**
    - `adminRules` — array
      - _array of_ `object`
        - `subject` — string **(required)**
        - `operation` — string **(required)** _(enum: `epbx`, `noepbx`, `egroup`, `noegroup`, `epage`, `noepage`, `eperm`, `noeperm`)_
- Errors: `400`, `401`, `403`, `500`

#### `DELETE` `/PBX/AclGroups/{groupIds}/`

**Delete ACL groups**

This endpoint is available only to the user who has "admin" username.

- operationId: `deletePBXAclGroups`
- **Parameters**
  - `groupIds` (path) — array **(required)**
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — any **(required)**
  - `code` — string
  - `reason` — string
  - `errors` — object
    - `parameter1` — object
      - `code` — string
      - `reason` — string
    - `parameter2` — object
      - `code` — string
      - `reason` — string
    - `parameterN` — object
      - `code` — string
      - `reason` — string
- Errors: `400`, `401`, `403`, `500`

#### `PUT` `/PBX/AclGroups/{groupId}/`

**Modify an ACL group**

To a user with "admin" username, all fields of this endpoint are available. To other admins who can manage a group, only "rules" field is available.

- operationId: `modifyPBXAclGroup`
- **Parameters**
  - `groupId` (path) — integer **(required)** — An identifier of the group. _(format=int32)_
- **Request body** (`application/json`)
  - `name` — string — This property can't be empty.
  - `wcgrp` — integer — To remove this property, you need to send an empty value for it. _(format=int32)_
  - `inhetits[dn]` — string — A DN of a parent group. To remove it, send an empty value for top-level of property (ex. inherits=).
  - `rules[<index>][rule]` — string — A rule from the list of available rules.
  - `rules[<index>][ability]` — string _(enum: `True`, `False`, `set`, `noset`, `use`, `nouse`, `call`, `nocall`)_
  - `rules[<index>][group]` — string — A group DN to which this rule applies.
  - `adminRules[<index>][subject]` — string — A rule from the admin list of available rules.
  - `adminRules[<index>][operation]` — string _(enum: `epbx`, `noepbx`, `egroup`, `noegroup`, `epage`, `noepage`, `eperm`, `noeperm`)_
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`, `500`

#### `GET` `/PBX/AclGroups/Rules/`

**Get a list of available ACL rules**

Any authorized user can use this endpoint to get a full list of available ACL rules

- operationId: `getPBXAclGroupsRules`
- **Scopes**: `aclgroups:read`, `pbx:read`
- **Company API Key scope**: `aclgroups:read`
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `list` — array **(required)**
      - _array of_ `object`
        - `ability` — array **(required)**
          - _array of_ `string`
        - `access` — array **(required)**
          - _array of_ `object`
            - `key` — string **(required)**
            - `name` — string **(required)**
            - `group` — boolean **(required)**
    - `default` — array **(required)**
      - _array of_ `object`
        - `rule` — string **(required)**
        - `ability` — string **(required)** _(enum: `True`, `False`, `set`, `noset`, `use`, `nouse`, `call`, `nocall`)_
        - `group` — string **(required)**
    - `adminList` — array **(required)**
      - _array of_ `object`
        - `ability` — array **(required)**
          - _array of_ `string`
        - `access` — array **(required)**
          - _array of_ `object`
            - `name` — string **(required)**
            - `subject` — string **(required)**
- Errors: `401`, `403`, `500`

#### `GET` `/PBX/AclGroups/Permissions/`

**Get a list of group permissions**

Any authorized user can use this endpoint to get a list of group permissions

- operationId: `getPBXAclGroupsPermissions`
- **Scopes**: `aclgroups:read`, `pbx:read`
- **Company API Key scope**: `aclgroups:read`
- **Parameters**
  - `groups` (query) — array — User group(s) ID for filter result. Example: ['12345'] or ['12345','67890','134711']
  - `permissions` (query) — array — ACL permission(s) key for filter result. Example: ['SEE_CALL_RECORDINGS'] or ['CTI_ANALYTICS','SUPERVISION','SEE_ANALYTICS']
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — array **(required)**
    - _array of_ `object`
      - `ability` — array — Permission type
        - _array of_ `string`
      - `key` — string — Permission key
      - `name` — string — Permission name
      - `containSubGroups` — boolean — Contain or not subgroups
      - `groups` — array
        - _array of_ `object`
          - `groupDn` — string — PBX group dn
          - `groupName` — string — PBX group name
          - `access` — string — Allow or not access for this permission
          - `subGroups` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
- Errors: `401`, `403`, `500`

#### `GET` `/PBX/ping/`

Check PBX availability

- operationId: `getPing`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=Pong)_

#### `GET` `/PBX/candidates`

Get PBX candidates

- operationId: `getCandidates`
- **Scopes**: `info:read`, `pbx:read`
- **Company API Key scope**: `info:read`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `networkAddresses` — array _(default=['krzhevitskywms4.wildixin.com'])_
      - _array of_ `any`
    - `ports` — array _(default=['443'])_
      - _array of_ `any`
    - `failovers` — array _(default=[])_
      - _array of_ `any`
- Errors: `401`, `403`, `500`

#### `GET` `/PBX/Ports/Status/`

**Get status of PBX open ports**

Get the status of open ports of the PBX

- operationId: `getPortsStatus`
- **Scopes**: `info:read`, `pbx:read`
- **Company API Key scope**: `info:read`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — int _(default=7)_
    - `records` — array
      - _array of_ `object`
        - `port` — string
        - `transport` — string
        - `protocol` — string
        - `status` — string
        - `lastcheck` — string
- Errors: `401`, `403`, `500`

#### `GET` `/PBX/version/`

**Get PBX version**

Returns the PBX version

- operationId: `getVersion`
- **Scopes**: `info:read`, `pbx:read`
- **Company API Key scope**: `info:read`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=3.40.27805.1)_
- Errors: `401`, `403`

#### `GET` `/PBX/settings/`

**Get PBX settings**

Returns settings of the PBX

- operationId: `pbxSettings`
- **Response 200**
  - `type` — string _(enum: `result`)_
  - `result` — object
    - `host` — string — PBX hostname
    - `customSecurePort` — int — Customer secure port
    - `tlsVersion` — string — TLS version
    - `wmsNetworkRole` — string — WMS network role _(enum: `master`, `slave`, `null`)_
    - `version` — string — WMS version
    - `isCloud` — boolean — Is cloud flag
    - `pbxName` — string — PBX name
    - `pbxSerial` — string — PBX serial
    - `pbxDn` — string — PBX dn
    - `defaultLanguage` — string — PBX language
    - `isUserDirMounted` — boolean — Is user directory mounted flag
    - `isBackupsMounted` — boolean — Is backups directory mounted flag
    - `partnerLogo` — string — Relative path to the partner custom logo, empty string if not set
    - `hardware` — object
      - `isPower` — boolean — Is PBX powerful flag
      - `processor` — string — PBX processor model
      - `memory` — string — PBX memory
    - `integrations` — array
      - _array of_ `object`
        - `name` — string — Integration name
        - `enabled` — boolean — Is integration enabled flag
    - `license` — object
      - `xbees` — boolean
      - `wmsNetwork` — boolean
      - `classound` — boolean
      - `microsoftPhoneSystem` — boolean
      - `xcaracal` — boolean
      - `maximumAvailableLicenseType` — string
      - `activated` — boolean
      - `subscription` — boolean
    - `cdrSettings` — object
      - `selectedBackend` — string — Selected backend for CDR _(enum: `mysql`, `sqlite`, `mssql`)_
      - `tags` — array
        - _array of_ `string`
      - `contactNotes` — boolean — Is contact notes enabled flag
      - `hideInCdrView` — int
      - `deleteCallsAfter` — int
      - `deleteChatsAfter` — int
      - `deleteVoicemailAfter` — int
      - `deleteRecordingAfter` — int
      - `allowCustomTags` — boolean — Allow adding custom tags during active call
    - `features` — array
      - _array of_ `object`
        - `name` — string, _(enum: `mfa`, `cloudAnalytics`, `callControl`, `allowCollaboration6`, `keepCallDialogAfterCall`, `sms`, `zabbixAgent`, `xcaracal`)_
        - `label` — string
        - `enabled` — boolean
        - `available` — boolean — If true, this feature can be configured
        - `isServerManagement` — boolean — Allow this feature to be configured only on WMS Network Server PBX
        - `hint` — string
        - `error` — string — Why an enabled feature is not working, for example a service that is installed and enabled but not running. Absent while the feature is healthy.
        - `message` — string — What is being done to the feature right now, while the change is applied in the background. Present only while it is in flight; the `enabled` field then reports the requested state, not the current one.
        - `database` — object — x-caracal only, on an on-premise PBX while it is enabled: the database it works with. The password is never returned.
          - `host` — string
          - `name` — string
          - `user` — string
    - `networkInterfaces` — array
      - _array of_ `object`
        - `name` — string
        - `type` — string
        - `address` — string
        - `netmask` — string
        - `activate` — string _(enum: `UP`, `DOWN`)_
        - `broadcast` — string
        - `network` — string
        - `alias` — string
        - `link` — string
    - `userSyncSettings` — object
      - `job` — object
        - `enabled` — boolean
        - `interval` — int
        - `email` — string
- Errors: `401`, `403`

#### `PUT` `/PBX/settings/`

**Update PBX Feature settings**

Update PBX settings. Currently supports updating feature flags.

Only one feature can be updated per request (batch operations are not supported).

****Available only for administrators****

- operationId: `pbxSettingsPut`
- **Request body** (`application/json`) **(required)**
  - `features` — array **(required)** — Array with a single feature object to update _(maxItems=1)_
    - _array of_ `object`
      - `name` — string **(required)** — Feature name _(enum: `callControl`, `cloudAnalytics`, `mfa`, `allowCollaboration6`, `keepCallDialogAfterCall`, `sms`, `zabbixAgent`, `xcaracal`)_
      - `enabled` — boolean **(required)** — Whether the feature is enabled
      - `database` — object — x-caracal only, on an on-premise PBX: the database x-caracal is enabled with. A cloud PBX always uses the local one.
        - `host` — string
        - `name` — string
        - `user` — string
        - `password` — string
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`, `501`

#### `GET` `/PBX/recordings/`

**Get list of all call recordings**

Returns list of all call recordings
<p style="color:red">Available only for user admin (root)</p>

- operationId: `pbxRecordings`
- **Scopes**: `recordings:read`, `pbx:read`
- **Company API Key scope**: `recordings:read`
- **Parameters**
  - `count` (query) — integer
  - `start` (query) — string
  - `from` (query) — integer
  - `to` (query) — integer
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `items` — array
      - _array of_ `object`
        - `path` — string — Recording path
        - `created` — int
        - `size` — int
    - `nextPage` — string — If field is empty, there are no more results for the current request.
- Errors: `401`, `403`

#### `GET` `/PBX/recordings/download/{id}`

**Get status of download recordings task**

Returns status of task for downloading batch of recordings
<p style="color:red">Available only for user admin (root)</p>

- operationId: `getStatusRecordingsTask`
- **Scopes**: `recordings:read`, `pbx:read`
- **Company API Key scope**: `recordings:read`
- **Parameters**
  - `id` (path) — string **(required)**
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `status` — string
    - `path` — string
- Errors: `401`, `403`

#### `POST` `/PBX/recordings/download/`

**Create task to download batch of recordings**

Returns an id of task and to and from values for downloading batch of recordings
<p style="color:red">Available only for user admin (root)</p>

- operationId: `createDownloadRecordingsTask`
- **Scopes**: `recordings:*`, `pbx:*`
- **Company API Key scope**: `recordings:*`
- **Request body** (`application/json`)
  - `from` — integer
  - `to` — integer
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `id` — string
    - `to` — integer
    - `from` — integer
- Errors: `401`, `403`

### Call History

#### `GET` `/PBX/CallHistory/`

**Get full call history**

Admin can use this endpoint to get all call history from the PBX.
****Available only for administrators****

- operationId: `getPBXCallHistory`
- **Scopes**: `callhistory:read`, `pbx:read`
- **Company API Key scope**: `callhistory:read`
- **Parameters**
  - `None` (None) — string
- **Response 200** (`CallHistory`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `total` — integer **(required)**
    - `records` — array **(required)**
      - _array of_ `object`
        - `id` — string
        - `start` — string
        - `answer` — string
        - `end` — string
        - `src` — string
        - `dst` — string
        - `from_number` — string
        - `to_number` — string
        - `from_name` — string
        - `to_name` — string
        - `billsec` — string
        - `disposition` — string _(enum: `NO ANSWER`, `ANSWERED`, `BUSY`)_
        - `lastapp` — string
        - `userfield` — string
        - `faxdata` — string
        - `lastdata` — string
        - `cost` — string
        - `organization` — string
        - `channel` — string
        - `dstchannel` — string
        - `app` — string
        - `callclass` — string
        - `dest_type` — string
        - `duration` — string
        - `dcontext` — string
        - `pbxid` — string
        - `type` — string _(enum: `call`, `fax`, `voicemail`)_
        - `attachments` — object — Voice mail, recordings, faxes info
          - `vm` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `recordings` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `faxes` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `timezone` — string **(required)**
- Errors: `401`, `403`, `500`

#### `GET` `/CallHistory/`

**Get personal call history**

Get call history for current authorized user

- operationId: `getCallHistory`
- **Parameters**
  - `None` (None) — string
- **Response 200** (`CallHistory`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `total` — integer **(required)**
    - `records` — array **(required)**
      - _array of_ `object`
        - `id` — string
        - `start` — string
        - `answer` — string
        - `end` — string
        - `src` — string
        - `dst` — string
        - `from_number` — string
        - `to_number` — string
        - `from_name` — string
        - `to_name` — string
        - `billsec` — string
        - `disposition` — string _(enum: `NO ANSWER`, `ANSWERED`, `BUSY`)_
        - `lastapp` — string
        - `userfield` — string
        - `faxdata` — string
        - `lastdata` — string
        - `cost` — string
        - `organization` — string
        - `channel` — string
        - `dstchannel` — string
        - `app` — string
        - `callclass` — string
        - `dest_type` — string
        - `duration` — string
        - `dcontext` — string
        - `pbxid` — string
        - `type` — string _(enum: `call`, `fax`, `voicemail`)_
        - `attachments` — object — Voice mail, recordings, faxes info
          - `vm` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `recordings` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `faxes` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `timezone` — string **(required)**
- Errors: `401`, `403`, `500`

#### `GET` `/CallHistory/{callId}`

**Get call record**

Get call record by ID

- operationId: `getCallHistoryRecord`
- **Parameters**
  - `callId` (path) — integer **(required)**
  - `None` (None) — string
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `id` — string
    - `start` — string
    - `answer` — string
    - `end` — string
    - `src` — string
    - `dst` — string
    - `from_number` — string
    - `to_number` — string
    - `from_name` — string
    - `to_name` — string
    - `billsec` — string
    - `disposition` — string _(enum: `NO ANSWER`, `ANSWERED`, `BUSY`)_
    - `lastapp` — string
    - `userfield` — string
    - `faxdata` — string
    - `lastdata` — string
    - `cost` — string
    - `organization` — string
    - `channel` — string
    - `dstchannel` — string
    - `app` — string
    - `callclass` — string
    - `dest_type` — string
    - `duration` — string
    - `dcontext` — string
    - `pbxid` — string
    - `type` — string _(enum: `call`, `fax`, `voicemail`)_
    - `attachments` — object — Voice mail, recordings, faxes info
      - `vm` — array
        - _array of_ `object`
          - `url` — string — full path for voice mail
      - `recordings` — array
        - _array of_ `object`
          - `url` — string — full path for recordings
          - `time` — integer — timestamp
          - `source` — string
          - `destination` — string
      - `faxes` — array
        - _array of_ `object`
          - `url` — string — full path for faxes
    - `timezone` — string **(required)**
- Errors: `401`, `403`, `404`, `500`

#### `PUT` `/CallHistory/{callId}`

**Update archived status**

Updates archived status for a call record.

- operationId: `updateCallHistoryRecord`
- **Parameters**
  - `callId` (path) — integer **(required)**
- **Request body** (`application/json`) **(required)**
  - `data[archived]` — string **(required)** — Archived status _(enum: `True`, `False`)_
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `changed` — integer — Changed record _(default=1)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `DELETE` `/CallHistory/{callId}`

**Delete call record**

Deletes call record by ID

- operationId: `deleteCallHistoryRecord`
- **Parameters**
  - `callId` (path) — integer **(required)**
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `deleted` — integer — Deleted record _(default=1)_
- Errors: `400`, `401`, `403`, `500`

#### `PUT` `/CallHistory/{callId}/Tags/`

**Change tags**

Changes tags for a call record

- operationId: `updateCallHistoryRecordTags`
- **Parameters**
  - `callId` (path) — integer **(required)**
- **Request body** (`application/json`) **(required)**
  - `tags` — string **(required)** — Tags (comma-separated) ##### Tag can contain digits (0-9), uppercase (A-Z), lowercase (a-z) letters, underscore (_) and hyphen, minus, dash (-)
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — string **(required)** _(default=Success)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `PUT` `/CallHistory/{callId}/Voicemail/`

**Update voicemails status**

Marks voicemail as read

- operationId: `updateCallHistoryVoicemail`
- **Parameters**
  - `callId` (path) — integer **(required)**
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — string **(required)** _(default=Success)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `DELETE` `/CallHistory/{callId}/Voicemail/`

**Delete voicemails**

Deletes voicemail from call record.

- operationId: `deleteCallHistoryVoicemail`
- **Parameters**
  - `callId` (path) — integer **(required)**
- **Response 200**
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — string **(required)** _(default=Success)_
- Errors: `400`, `401`, `403`, `404`, `500`

#### `GET` `/User/{extension}/CallHistory/`

**Get call history by user**

Returns call history by user.
****Available only for administrators****

- operationId: `getCallHistoryByUser`
- **Parameters**
  - `extension` (path) — integer **(required)** — User extension
  - `None` (None) — string
- **Response 200** (`CallHistory`)
  - `type` — string **(required)** _(enum: `result`)_
  - `result` — object **(required)**
    - `total` — integer **(required)**
    - `records` — array **(required)**
      - _array of_ `object`
        - `id` — string
        - `start` — string
        - `answer` — string
        - `end` — string
        - `src` — string
        - `dst` — string
        - `from_number` — string
        - `to_number` — string
        - `from_name` — string
        - `to_name` — string
        - `billsec` — string
        - `disposition` — string _(enum: `NO ANSWER`, `ANSWERED`, `BUSY`)_
        - `lastapp` — string
        - `userfield` — string
        - `faxdata` — string
        - `lastdata` — string
        - `cost` — string
        - `organization` — string
        - `channel` — string
        - `dstchannel` — string
        - `app` — string
        - `callclass` — string
        - `dest_type` — string
        - `duration` — string
        - `dcontext` — string
        - `pbxid` — string
        - `type` — string _(enum: `call`, `fax`, `voicemail`)_
        - `attachments` — object — Voice mail, recordings, faxes info
          - `vm` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `recordings` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `faxes` — array
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `timezone` — string **(required)**
- Errors: `401`, `403`, `404`, `500`

### Voicemail

#### `GET` `/VoiceMail/`

**Get all voicemails from PBX**

Get all voicemails from the PBX (available from WMS v. 3.80.30805.52)

- operationId: `getVoiceMail`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — string
    - `records` — array
      - _array of_ `object`
        - `duration` — string
        - `macrocontext` — string
        - `flag` — string
        - `origdate` — string
        - `origtime` — string
        - `exten` — string
        - `rdnis` — string
        - `category` — string
        - `msg_id` — string
        - `origmailbox` — string
        - `callerchan` — string
        - `priority` — string
        - `context` — string
        - `callerid` — string
        - `folder` — string
        - `file` — string
        - `path` — string
- Errors: `401`, `500`

#### `PUT` `/VoiceMail/{id}/`

**Mark voicemail as read**

Marks voicemail as read

- operationId: `putVoiceMail`
- **Request body** (`application/json`)
  - `data[folder]` — array
    - _array of_ `any`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `errors` — array
      - _array of_ `object`
        - `msg1452512084-2115301175` — string
        - `msg1452512018-1778991337` — string
    - `changed` — int _(default=0)_
- Errors: `401`, `500`

#### `DELETE` `/VoiceMail/{ids}/`

Delete voicemail

- operationId: `deleteVoiceMail`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `errors` — array _(default=[])_
      - _array of_ `any`
    - `changed` — int _(default=2)_
- Errors: `401`, `500`

### TrustedIP

#### `GET` `/TrustedIP/`

**Get all trusted IPs for PBX**

Returns all trusted IPs for the PBX

- operationId: `getTrustedIP`
- **Response 200** (`list`)
  - `type` — string _(default=result)_
  - `result` — object
    - `rows` — array — List of IPs
      - _array of_ `string`
- Errors: `401`, `500`

#### `PUT` `/TrustedIP/`

**Set trusted IP for PBX**

Sets trusted IP for the PBX

- operationId: `putTrustedIP`
- **Request body** (`application/json`)
  - `rows` — array — List of IPs
    - _array of_ `any`
- **Response 200** (`list`)
  - `type` — string _(default=result)_
  - `result` — object
    - `rows` — array — List of IPs
      - _array of_ `string`
- Errors: `400`, `401`, `500`

### Call Queue

#### `GET` `/PBX/settings/CallQueues/`

**Get a list of call Queues**

****Available only for administrators****

- operationId: `pbxSettingsGetCallQueues`
- **Scopes**: `callgroups:read`, `pbx:read`
- **Company API Key scope**: `callgroups:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer
        - `name` — string
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `GET` `/PBX/settings/CallQueues/{id}/`

**Get call Queue**

****Available only for administrators****

- operationId: `pbxSettingsGetCallQueue`
- **Scopes**: `callgroups:read`, `pbx:read`
- **Company API Key scope**: `callgroups:read`
- **Parameters**
  - `id` (path) — integer **(required)**
- **Response 200**
  - `result` — object
    - `id` — integer
    - `name` — string
    - `members` — array
      - _array of_ `object`
        - `name` — string
        - `stateInterface` — string
        - `membership` — string
        - `penalty` — string
        - `callsTaken` — string
        - `lastCall` — string
        - `isInCall` — string
        - `status` — string
        - `paused` — string
        - `actionID` — string
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/PBX/settings/CallQueues/{id}/members/dynamic/`

**Add a dynamic member to call Queue**

****Available only for administrators****

- operationId: `pbxSettingsAddMemberDynamicToCallQueue`
- **Scopes**: `callgroups:*`, `pbx:*`
- **Company API Key scope**: `callgroups:*`
- **Request body** (`application/json`) **(required)**
  - `member` — string **(required)** — Member
  - `penalty` — integer — Penalty
  - `paused` — integer — Paused _(enum: `0`, `1`)_
- **Response 200**
  - `result` — object
    - `Message` — string _(default=Added interface to queue)_
    - `Response` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/PBX/settings/CallQueues/{id}/members/dynamic/{member}`

**Delete a dynamic member from call Queue**

****Available only for administrators****

- operationId: `pbxSettingsDeleteMemberDynamicFromCallQueue`
- **Scopes**: `callgroups:*`, `pbx:*`
- **Company API Key scope**: `callgroups:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Queue ID
  - `member` (path) — string **(required)** — Member **Need to encode special charset to URI format**
- **Response 200**
  - `result` — object
    - `Message` — string _(default=Removed interface from queue)_
    - `Response` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Call Group Management

#### `POST` `/api/v2/call-groups/{id}/members/dynamic/`

**Add a dynamic member to a Call Group**

Allows delegated managers to add a dynamic member to a Call Group.
Available only for users that have the `MANAGE_CALLGROUP` permission on the ACL group linked to the target Call Group via `settings.aclGroup`.

- operationId: `callGroupsAddDynamicMember`
- **Parameters**
  - `id` (path) — integer **(required)** — Call Group ID
- **Request body** (`application/json`) **(required)**
  - `member` — string **(required)** — Member
  - `penalty` — integer — Penalty
  - `paused` — integer — Paused _(enum: `0`, `1`)_
- **Response 200**
  - `result` — object
    - `Message` — string _(default=Added interface to queue)_
    - `Response` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/api/v2/call-groups/{id}/forward/`

**Forward a call in a Call Group queue**

Allows delegated managers to forward an active call in a Call Group queue.
Available only for users that have the `MANAGE_CALLGROUP` permission on the ACL group linked to the target Call Group via `settings.aclGroup`.

A `400` response can mean either request validation failed (`errors` object) or the PBX/Callweaver rejected the AMI forward command; in the latter case `reason` is the message returned by the PBX (for example `Channel not found`) and `code` is `ForwardOperationFailed`.

An unexpected failure while executing the request (for example an exception from the PBX layer) is answered with HTTP `500`. The global error handler then typically exposes `InternalServerError` to the client while the failure is logged server-side.

- operationId: `callGroupsForwardCall`
- **Parameters**
  - `id` (path) — integer **(required)** — Call Group ID
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP Call ID of an active queue call to forward _(maxLen=100)_
  - `destination` — string **(required)** — Extension or destination number to forward the call to _(maxLen=100)_
- **Response 200**
  - `result` — object
    - `message` — string _(default=Forward completed successfully)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`, `500`

#### `DELETE` `/api/v2/call-groups/{id}/members/dynamic/{member}`

**Delete a dynamic member from a Call Group**

Allows delegated managers to remove a dynamic member from a Call Group.
Available only for users that have the `MANAGE_CALLGROUP` permission on the ACL group linked to the target Call Group via `settings.aclGroup`.

- operationId: `callGroupsDeleteDynamicMember`
- **Parameters**
  - `id` (path) — integer **(required)** — Call Group ID
  - `member` (path) — string **(required)** — Member **Need to encode special charset to URI format**
- **Response 200**
  - `result` — object
    - `Message` — string _(default=Removed interface from queue)_
    - `Response` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

### Device

#### `POST` `/Device/ResetToken/`

**Reset a device token**

Used to reset a Wizyconf device token for reprovisioning

- operationId: `resetDeviceToken`
- **Scopes**: `devices:*`, `pbx:*`
- **Company API Key scope**: `devices:*`
- **Request body** (`application/json`)
  - `pin` — string
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `403`, `404`, `500`

### Devices

#### `GET` `/Devices/`

**Get devices**

Get devices list

- operationId: `getDevices`
- **Scopes**: `devices:read`, `pbx:read`
- **Company API Key scope**: `devices:read`
- **Parameters**
  - `count` (query) — integer — Maximum number of characters in the result output.
  - `start` (query) — integer — The result offset.
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Device id.
        - `mac` — string — Device mac address.
        - `model` — string — Device model line.
        - `description` — string — Device description .
        - `firmware` — string — Device firmware.
        - `alternatePort` — string — Alternate port.
        - `user` — string — An extension of the user assigned to device.
        - `address` — string — Device IP address.
        - `token` — string — Device password.
        - `allowAssign` — boolean — Allowed assigned user[s] to device.
        - `qtyPorts` — integer — Quantity port.
        - `multipleUsers` — array — Extensions of the users assigned to device.
          - _array of_ `any`
        - `ssl` — boolean — Use ssl.
        - `registrar` — object
          - `address` — string
          - `port` — string
        - `vendor` — object
          - `additional` — string
          - `name` — string
        - `provision` — boolean — Device provision.
        - `state` — string — Device state.
        - `settings` — object
          - `useStaticIp` — boolean
          - `useDst` — boolean
          - `syslogServer` — string
          - `dns` — object
            - `primary` — string
            - `secondary` — string
          - `voiceVLAN` — object
            - `voice` — string
            - `data` — integer
          - `dataVLAN` — object
            - `voice` — string
            - `data` — integer
          - `ntp` — object
            - `server` — string
            - `timezone` — string
        - `isOnline` — bool — Device online.
        - `isLocal` — bool — Device in local network.
        - `received` — string — Device received.
- Errors: `401`, `403`

#### `POST` `/Devices/`

**Add devices**

Adds devices by MAC address list

- operationId: `addDevices`
- **Scopes**: `devices:*`, `pbx:*`
- **Company API Key scope**: `devices:*`
- **Request body** (`application/json`) **(required)**
  - `macs` — array **(required)** — Array of MAC addresses.
    - _array of_ `any`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `records` — array — Device items.
      - _array of_ `object`
        - `mac` — string — Device mac address.
        - `value` — object
          - `mac` — string — Device mac address.
          - `model` — string — Device model line.
          - `vendor` — string — Device vendor.
          - `url` — string — Url to autoupdate.
- Errors: `400`, `401`, `403`

#### `PUT` `/Devices/{macAddr}/`

**Update device**

Update device by MAC address.

- operationId: `updateDevice`
- **Parameters**
  - `macAddr` (path) — string **(required)** — Device MAC address.
  - `description` (formData) — string — Device description.
  - `settings[dns][primary]` (formData) — string — Primary DNS server.
  - `settings[dns][secondary]` (formData) — string — Secondary DNS server.
  - `settings[voiceVLAN][voice]` (formData) — string — QOS voiceVLAN voice.
  - `settings[voiceVLAN][data]` (formData) — string — QOS voiceVLAN data.
  - `settings[dataVLAN][voice]` (formData) — string — QOS dataVLAN voice.
  - `settings[dataVLAN][data]` (formData) — string — QOS dataVLAN data.
  - `settings[ntp][server]` (formData) — string — Time server.
  - `settings[ntp][timezone]` (formData) — string — Time zone.
  - `settings[syslogServer]` (formData) — string — Log server.
  - `settings[useDst]` (formData) — string — Use Daylight Saving Time.
  - `settings[useStaticIp]` (formData) — string — Use static IP.
  - `settings[snmp]` (formData) — string — SNMP settings.
  - `user` (formData) — string — User extension.
  - `token` (formData) — string — Reset token.
  - `multipleUsers` (formData) — string — Users extension.
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`

#### `DELETE` `/Devices/{macAddr}/`

**Delete device**

Delete device by mac address

- operationId: `deleteDevice`
- **Parameters**
  - `macAddress` (path) — string **(required)** — Device mac address.
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`

#### `POST` `/Devices/scan/`

**Scan devices**

Scans devices

- operationId: `scanDevice`
- **Scopes**: `devices:*`, `pbx:*`
- **Company API Key scope**: `devices:*`
- **Request body** (`application/json`) **(required)**
  - `range` — string **(required)** — Device IP address.
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `address` — integer — Device address.
        - `port` — string — Device port.
- Errors: `400`, `401`, `403`

#### `GET` `/Devices/verify/`

**Verify devices**

Verifies devices

- operationId: `verifyDevice`
- **Scopes**: `devices:read`, `pbx:read`
- **Company API Key scope**: `devices:read`
- **Request body** (`application/json`) **(required)**
  - `range` — string **(required)** — Device IP address.
  - `port` — string **(required)** — Device IP address.
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `allow` — bool — Allow provision.
    - `address` — string — Device IP address.
    - `mac` — string — Device mac address.
    - `model` — string — Device model.
    - `port` — string — Device port.
- Errors: `400`, `401`, `403`

#### `POST` `/Devices/{macAddr}/connect/`

**Connect device**

Connects a device.

- operationId: `connectDevice`
- **Parameters**
  - `macAddress` (path) — string **(required)** — Device MAC address.
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `dump` — string — Dump version.
    - `host` — string — Device IP address.
    - `name` — string
    - `opt` — string — Device link.
    - `port` — string — Device port.
    - `ssl` — string — Device use ssl.
- Errors: `400`, `401`

#### `DELETE` `/Devices/{macAddr}/connect/`

**Disconnect device**

Disconnects a device.

- operationId: `disconnectDevice`
- **Parameters**
  - `macAddress` (path) — string **(required)** — Device MAC address.
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`

### Dialplans

#### `GET` `/PBX/Dialplans/`

**Get a list of Dialplans**

Returns the list of all available Dialplans on the PBX

- operationId: `pbxSettingsGetDialplans`
- **Scopes**: `dialplan:read`, `pbx:read`
- **Company API Key scope**: `dialplan:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Dialplan ID
        - `name` — string — Dialplan name
        - `description` — string — Dialplan description
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/PBX/Dialplans/`

**Add new a Dialplan**

**Company API Key:** supported.

- operationId: `pbxSettingsCreateDialplan`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Request body** (`application/json`)
  - `name` — string — Dialplan name (required)
  - `description` — string — Dialplan description
  - `numbers` — array — List of numbers
    - _array of_ `DialplanItemNumber`
      - `number` — string — Rule number
      - `apps` — array — List of rules
        - _array of_ `object`
          - `name` — string — Application name (key) https://wildix.atlassian.net/wiki/x/ahDOAQ _(enum: `Answer`, `AsrIvr`, `AuthenticateUser`, `Background`, `Callback`, `Conference`, `CorrectOutgoingNumber`, `CustomApp`, `DialHuntGroup`, `DialPhone`, `DialRemotePbx`, `DialTrunk`, … (+30))_
          - `params` — object — List of application params (allowed empty)
            - `key_1` — string — value 1
            - `key_2` — string — value 2
            - `key_N` — string — value N
      - `comment` — string — Comment
  - `includedDialplans` — array — List of included Dialplans (can be empty)
    - _array of_ `DialplanItemIncludes`
      - `dialplanId` — integer — Dialplan ID. Allowed numbers greater or less zero
- **Response 200**
  - `result` — DialplanItem
    - `id` — integer — Dialplan ID
    - `name` — string — Dialplan name
    - `description` — string — Dialplan description
    - `numbers` — array — List of numbers
      - _array of_ `object`
        - `number` — string — Rule number
        - `apps` — array — List of rules
          - _array of_ `object`
            - `name` — string — Application name (key) https://wildix.atlassian.net/wiki/x/ahDOAQ _(enum: `Answer`, `AsrIvr`, `AuthenticateUser`, `Background`, `Callback`, `Conference`, `CorrectOutgoingNumber`, `CustomApp`, `DialHuntGroup`, `DialPhone`, `DialRemotePbx`, `DialTrunk`, … (+30))_
            - `params` — object — List of application params (allowed empty)
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `comment` — string — Comment
    - `includedDialplans` — array — List of included Dialplans (can be empty)
      - _array of_ `object`
        - `dialplanId` — integer — Dialplan ID. Allowed numbers greater or less zero
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `GET` `/PBX/Dialplans/{id}/`

**Get Dialplan**

Returns Dialplan info

- operationId: `pbxSettingsGetDialplan`
- **Scopes**: `dialplan:read`, `pbx:read`
- **Company API Key scope**: `dialplan:read`
- **Parameters**
  - `id` (path) — integer **(required)** — Dialplan ID
- **Response 200**
  - `result` — DialplanItem
    - `id` — integer — Dialplan ID
    - `name` — string — Dialplan name
    - `description` — string — Dialplan description
    - `numbers` — array — List of numbers
      - _array of_ `object`
        - `number` — string — Rule number
        - `apps` — array — List of rules
          - _array of_ `object`
            - `name` — string — Application name (key) https://wildix.atlassian.net/wiki/x/ahDOAQ _(enum: `Answer`, `AsrIvr`, `AuthenticateUser`, `Background`, `Callback`, `Conference`, `CorrectOutgoingNumber`, `CustomApp`, `DialHuntGroup`, `DialPhone`, `DialRemotePbx`, `DialTrunk`, … (+30))_
            - `params` — object — List of application params (allowed empty)
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `comment` — string — Comment
    - `includedDialplans` — array — List of included Dialplans (can be empty)
      - _array of_ `object`
        - `dialplanId` — integer — Dialplan ID. Allowed numbers greater or less zero
  - `type` — string _(default=result)_
- Errors: `401`, `403`, `404`

#### `PUT` `/PBX/Dialplans/{id}/`

**Update Dialplan**

**Company API Key:** supported.

- operationId: `pbxSettingsUpdateDialplan`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Dialplan ID
- **Request body** (`application/json`)
  - `description` — string — Dialplan description
  - `numbers` — array — List of numbers
    - _array of_ `DialplanItemNumber`
      - `number` — string — Rule number
      - `apps` — array — List of rules
        - _array of_ `object`
          - `name` — string — Application name (key) https://wildix.atlassian.net/wiki/x/ahDOAQ _(enum: `Answer`, `AsrIvr`, `AuthenticateUser`, `Background`, `Callback`, `Conference`, `CorrectOutgoingNumber`, `CustomApp`, `DialHuntGroup`, `DialPhone`, `DialRemotePbx`, `DialTrunk`, … (+30))_
          - `params` — object — List of application params (allowed empty)
            - `key_1` — string — value 1
            - `key_2` — string — value 2
            - `key_N` — string — value N
      - `comment` — string — Comment
  - `includedDialplans` — array — List of included Dialplans (can be empty)
    - _array of_ `DialplanItemIncludes`
      - `dialplanId` — integer — Dialplan ID. Allowed numbers greater or less zero
- **Response 200**
  - `result` — DialplanItem
    - `id` — integer — Dialplan ID
    - `name` — string — Dialplan name
    - `description` — string — Dialplan description
    - `numbers` — array — List of numbers
      - _array of_ `object`
        - `number` — string — Rule number
        - `apps` — array — List of rules
          - _array of_ `object`
            - `name` — string — Application name (key) https://wildix.atlassian.net/wiki/x/ahDOAQ _(enum: `Answer`, `AsrIvr`, `AuthenticateUser`, `Background`, `Callback`, `Conference`, `CorrectOutgoingNumber`, `CustomApp`, `DialHuntGroup`, `DialPhone`, `DialRemotePbx`, `DialTrunk`, … (+30))_
            - `params` — object — List of application params (allowed empty)
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `comment` — string — Comment
    - `includedDialplans` — array — List of included Dialplans (can be empty)
      - _array of_ `object`
        - `dialplanId` — integer — Dialplan ID. Allowed numbers greater or less zero
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/PBX/Dialplans/{id}/`

**Delete Dialplan**

- operationId: `pbxSettingsDeleteDialplan`
- **Parameters**
  - `id` (path) — integer **(required)** — Dialplan ID
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/PBX/Dialplans/{ids}/`

**Delete Dialplans**

**Company API Key:** supported.

- operationId: `pbxSettingsDeleteDialplans`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — string **(required)** — List of Dialplan IDs, separated by commas
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Dialplan Paging Groups

#### `GET` `/Dialplan/PagingGroups/`

Get paging groups

- operationId: `getDialplansPagingGroups`
- **Scopes**: `dialplan:read`, `pbx:read`
- **Company API Key scope**: `dialplan:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Paging group id
        - `title` — string — Paging group name
        - `members` — array — Paging group members
          - _array of_ `any`
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/Dialplan/PagingGroups/`

**Add paging group**

Add a paging group by members

- operationId: `createDialplansPagingGroup`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Request body** (`application/json`) **(required)**
  - `title` — string **(required)** — Name of the paging group.
  - `members` — array **(required)** — Array of extentions.
    - _array of_ `any`
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Dialplan/PagingGroups/{id}/`

**Update paging group**

Returns Dialplan info

- operationId: `Paging group update`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Dialplan paging group ID
- **Request body** (`application/json`)
  - `title` — string — Paging group name.
  - `members[]` — array — Paging group members.
    - _array of_ `any`
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/Dialplan/PagingGroups/{id}/`

**Delete paging group**

Deletes paging group by ID

- operationId: `deletePagingGroup`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — string **(required)** — ID of the paging group.
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Dialplan General Settings

#### `GET` `/Dialplan/GeneralSettings/`

**Get general settings**

Returns the list of all available Dialplan general settings on the PBX

- operationId: `getDialplansGeneralSettings`
- **Scopes**: `dialplan:read`, `pbx:read`
- **Company API Key scope**: `dialplan:read`
- **Response 200**
  - `result` — object
    - `faxLang` — string — Fax language.
    - `parkTimeout` — integer — Park call timeout.
    - `prefixExtLine` — string — Prefix for external line.
    - `internationalPrefix` — string — International prefix.
    - `nationalPrefix` — string — National prefix.
    - `intDialTimeout` — string — Internal call default timeout.
    - `transferDigitTimeout` — string — First digit timeot (secs).
    - `transferInterDigitTimeout` — string — Interdigit timeout (secs).
    - `endOfDigit` — string — Send call key.
    - `buttonSound` — boolean — Playback tones while entering number.
    - `attachFormatVm` — string — Quality of recorded Voicemails.
    - `attachFormatRec` — string — Quality of call recordings.
    - `recNotify` — boolean — Send mail notification after the record is complete.
    - `recAttach` — boolean — Attach files with records to emails.
    - `faxAttach` — boolean — Attach fax files to email notifications.
    - `vmNotify` — boolean — Send mail notification about new voicemails.
    - `describeVoiceMail` — boolean — Convert Voicemails to text and send by email.
    - `trunkRegistrationNotification` — boolean — Notify by email in case SIP trunk registration status is changed.
    - `voiceMailMessageMoreInfo` — boolean — Announce date, time and caller phone number for Voicemail messages.
    - `userVariables` — string — Set dialplan variables.
    - `quickDialPatterns` — string
    - `personalRecordType` — string — Personal recording behavior mode. _(enum: `default`, `record`, `transcribe`, `record_transcribe`)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `PUT` `/Dialplan/GeneralSettings/`

**Update general settings**

Update the list of all available Dialplan general settings on the PBX

- operationId: `putDialplansGeneralSettings`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Request body** (`application/json`)
  - `faxLang` — string — A language code. Example: EN, IT, FR, DE, RN, BG, ES, NL, EN-US, EE
  - `parkTimeout` — integer — Timeout (secs). _(min=0; max=32767)_
  - `prefixExtLine` — string — A numeric string. _(minLen=0)_
  - `internationalPrefix` — string — A numeric string. _(minLen=0)_
  - `nationalPrefix` — string — A numeric string. _(minLen=0)_
  - `intDialTimeout` — string — A numeric string. _(minLen=10; maxLen=600)_
  - `transferDigitTimeout` — string **(required)** — A numeric string. _(minLen=0)_
  - `transferInterDigitTimeout` — string **(required)** — A numeric string. _(minLen=1; maxLen=12)_
  - `endOfDigit` — string — 0 - "None", 1 - "*", 2 - "&#35;". _(enum: `0`, `1`, `2`)_
  - `buttonSound` — boolean — Playback tones while entering number. _(enum: `True`, `False`)_
  - `attachFormatVm` — string — Quality of recorded Voicemails. _(enum: `mp3`, `wav`)_
  - `attachFormatRec` — string — Quality of call recordings. _(enum: `mp3`, `wav`)_
  - `recNotify` — boolean — Send mail notification after the record is complete. _(enum: `True`, `False`)_
  - `recAttach` — boolean — Attach files with records to emails. _(enum: `True`, `False`)_
  - `faxAttach` — boolean — Attach fax files to email notifications. _(enum: `True`, `False`)_
  - `vmNotify` — boolean — Send mail notification about new voicemails. _(enum: `True`, `False`)_
  - `describeVoiceMail` — boolean — Convert Voicemails to text and send by email. _(enum: `True`, `False`)_
  - `trunkRegistrationNotification` — boolean — Notify by email in case SIP trunk registration status is changed. _(enum: `True`, `False`)_
  - `voiceMailMessageMoreInfo` — boolean — Announce date, time and caller phone number for Voicemail messages. _(enum: `True`, `False`)_
  - `userVariables` — string — Custom user variables. Delimiter - &#92;n (new line). Example: VAR1=VAL1&#92;nVAR2=VAL2
  - `quickDialPatterns` — string — Set quick dial patterns. Delimiter - &#92;n (new line). Example: 1[0-9][0-9]&#92;n2[0-9][0-9]
  - `personalRecordType` — string — Personal recording behavior mode. Defines whether personal call recordings are recorded or recorded and transcribed. _(enum: `default`, `record`, `transcribe`, `record_transcribe`)_
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

### Dialplan Time Table

#### `GET` `/Dialplan/timeTables/`

**Get timetables**

Get the list of all Dialplan timetables on the PBX. Optionally filter by IDs

- operationId: `getDialplansTimeTables`
- **Scopes**: `dialplan:read`, `pbx:read`
- **Company API Key scope**: `dialplan:read`
- **Parameters**
  - `ids` (query) — array — Optional. List of timetable IDs to retrieve.
  - `responseType` (query) — string — Optional. Response type. If set to "file," the result will be downloaded as a JSON file. _(enum: `json`, `file`, `xml`)_
  - `filename` (query) — string — Optional. If responseType is "file," specifies the filename for the downloaded JSON file.
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `records` — array
      - _array of_ `TimeTables`
        - `id` — integer — Timetable ID
        - `title` — string — Timetable name
        - `state` — integer — Timetable state
        - `items` — object
          - `month` — integer — Mouth number.
          - `year` — integer — Year.
          - `from` — object
            - `day` — integer — Start day of month
            - `dayOfWeek` — integer — Start day of week
          - `to` — object
            - `day` — integer — End day of month
            - `dayOfWeek` — integer — End day of week
          - `time` — object
            - `from` — string — Start time
            - `to` — string — End time
- Errors: `401`, `403`

#### `POST` `/Dialplan/timeTables/`

**Add a timetable**

Create a new timetable

- operationId: `createDialplansTimeTables`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Request body** (`application/json`) **(required)**
  - `title` — string **(required)** — Timetable name.
  - `state` — integer **(required)** — State. _(enum: `0`, `1`, `2`)_
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Dialplan/timeTables/{id}/`

**Update timetable**

**Company API Key:** supported.

- operationId: `Timetable update`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Dialplan timetable ID
- **Request body** (`application/json`)
  - `title` — string — Timetable name.
  - `state` — integer — Timetable state. _(enum: `0`, `1`, `2`)_
  - `items[]` — array — Timetable items.
    - _array of_ `any`
  - `items[][from][day]` — integer **(required)** — Start day of the month.
  - `items[][from][dayOfWeek]` — integer **(required)** — Start day of the week.
  - `items[][to][day]` — integer **(required)** — End day of the month.
  - `items[][to][dayOfWeek]` — integer **(required)** — End day of the week.
  - `items[][time][from]` — string **(required)** — Start time.
  - `items[][time][to]` — string **(required)** — End time.
  - `items[][month]` — integer **(required)** — Month.
  - `items[][year]` — integer **(required)** — Year.
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/Dialplan/timeTables/{id}/`

**Delete timetable**

Delete timetable by ID

- operationId: `deleteTimeTable`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — integer **(required)** — ID of the timetable.
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Dialplan/timeTables/import/`

**Import timetables**

Import a list of timetables

- operationId: `importTimeTables`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Request body** (`application/json`) **(required)**
  - `records` — array
    - _array of_ `TimeTables`
      - `id` — integer — Timetable ID
      - `title` — string — Timetable name
      - `state` — integer — Timetable state
      - `items` — object
        - `month` — integer — Mouth number.
        - `year` — integer — Year.
        - `from` — object
          - `day` — integer — Start day of month
          - `dayOfWeek` — integer — Start day of week
        - `to` — object
          - `day` — integer — End day of month
          - `dayOfWeek` — integer — End day of week
        - `time` — object
          - `from` — string — Start time
          - `to` — string — End time
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Dialplan switches

#### `GET` `/Dialplan/Switches/`

**Get switches**

Get the list of all Dialplan switches on the PBX

- operationId: `getDialplansSwitches`
- **Scopes**: `dialplan:read`, `pbx:read`
- **Company API Key scope**: `dialplan:read`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Id
        - `title` — string — Name
        - `state` — integer — State
        - `isTreeType` — boolean — 3 states type
- Errors: `401`, `403`

#### `POST` `/Dialplan/Switches/`

**Add a switch**

Create a new switch

- operationId: `createDialplansSwitch`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Request body** (`application/json`) **(required)**
  - `title` — string **(required)** — Switch name.
  - `state` — integer **(required)** — state. _(enum: `0`, `1`, `2`)_
  - `isTreeType` — boolean **(required)** _(enum: `True`, `False`)_
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Dialplan/Switches/{id}/`

**Update switch**

**Company API Key:** supported.

- operationId: `switchUpdate`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Dialplan switch ID
- **Request body** (`application/json`)
  - `title` — string — Switch name.
  - `state` — integer — Switch state. _(enum: `0`, `1`, `2`)_
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/Dialplan/Switches/{id}/`

**Delete a switch**

Delete a switch by ID

- operationId: `deleteSwitch`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Switch ID.
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Dialplan IVR

#### `GET` `/Dialplan/Ivr/`

**Get IVR list**

Get the list of all available IVR on the PBX

- operationId: `getDialplansIvr`
- **Scopes**: `dialplan:read`, `pbx:read`
- **Company API Key scope**: `dialplan:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `IvrRoot`
        - `id` — integer — IVR ID
        - `title` — string — IVR name
        - `type` — string — Tree node type (menu or action) _(enum: `menu`, `item`)_
        - `parameters` — object — Menu parameters
          - `sound` — string **(required)** — Path to sound file
          - `times` — integer **(required)** — Number of times the audio file is played back to the caller
          - `timeout` — integer **(required)** — After this timeout in seconds, the Timeout action is performed
          - `backcode` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
          - `context` — string — Dialplan procedure
          - `exten` — string — Called number
        - `items` — array — Child elements (menu or item)
          - _array of_ `union`
            - _anyOf_ — one or more of:
              - **`Menu node`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`Action node`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/Dialplan/Ivr/`

**Create IVR**

Add a new IVR

- operationId: `createDialplansIvr`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Dialplan/Ivr/{id}/`

Update IVR

- operationId: `dialplansIvrUpdate`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/Dialplan/Ivr/{id}/`

**Delete IVR**

Delete IVR by ID

- operationId: `dialplansIvrDelete`
- **Scopes**: `dialplan:*`, `pbx:*`
- **Company API Key scope**: `dialplan:*`
- **Parameters**
  - `id` (path) — string **(required)** — IVR ID
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### Dialplan Call Groups

#### `GET` `/Dialplan/CallGroups/`

**Get Call groups**

Get the list of all available Call groups on the PBX

- operationId: `getDialplanCallGroups`
- **Scopes**: `callgroups:read`, `pbx:read`
- **Company API Key scope**: `callgroups:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Call group ID
        - `title` — string — Call group name
        - `members` — array — Members array. For priority strategy, priority is passed after member name, separated with comma: ['11@internalcalls,2']
          - _array of_ `any`
        - `settings` — object — Group settings
          - `queueManager` — string — Missed calls managers
          - `cid` — string — CID for outbound calls
          - `autoPause` — string — Auto pause on no answer _(default=False; enum: `False`, `True`, `all`)_
          - `autoPauseTime` — integer — Auto pause on no answer timeout _(default=5)_
          - `autoPauseDelay` — integer — Auto pause delay _(default=0)_
          - `autoPauseBusy` — boolean — Auto pause busy (readonly)
          - `autoPauseUnAvail` — boolean — Auto pause un avail (readonly)
          - `maxLen` — integer — Max length _(default=5)_
          - `retry` — integer — Seconds before recalling all the members again _(default=1)_
          - `ringInUse` — boolean — Call waiting _(default=False)_
          - `strategy` — string — Strategy _(default=ringall; enum: `ringall`, `priority`, `roundrobin`, `wringall`, `leastrecent`, `fewestcalls`, `linear`)_
          - `defaultPriority` — integer — Default priority used for dynamic call groups members. Works only for priority strategy. _(default=1; min=1; max=5)_
          - `timeout` — integer — Timeout (0 - 120) _(default=60)_
          - `weight` — integer — Priority _(default=0)_
          - `wrapUpTime` — integer — Wrap up time _(default=0)_
          - `rule` — string — Dialplan
          - `announce` — object
            - `frequency` — integer — Announce frequency _(default=0)_
            - `holdTime` — string — Announce hold time _(default=True; enum: `True`, `False`, `once`)_
            - `roundSeconds` — integer — Announce round seconds (readonly) _(default=5)_
          - `exitAllMembers` — object
            - `busy` — boolean — Exit if all members busy _(default=False)_
            - `paused` — boolean — Exit if all members paused / wrap up _(default=False)_
            - `ringing` — boolean — Exit if all members ringing _(default=False)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/Dialplan/CallGroups/`

**Create Call Group**

Add new Call Groups

- operationId: `createDialplansCallGroups`
- **Scopes**: `callgroups:*`, `pbx:*`
- **Company API Key scope**: `callgroups:*`
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Dialplan/CallGroups/{id}/`

**Update Call Group**

Update a Call Group

- operationId: `dialplanCallGroupUpdate`
- **Scopes**: `callgroups:*`, `pbx:*`
- **Company API Key scope**: `callgroups:*`
- **Parameters**
  - `id` (path) — string **(required)** — Call Group ID
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/Dialplan/CallGroups/{id}/`

**Delete Call Group**

Delete Call group by ID

- operationId: `dialplanCallGroupDelete`
- **Scopes**: `callgroups:*`, `pbx:*`
- **Company API Key scope**: `callgroups:*`
- **Parameters**
  - `id` (path) — string **(required)** — Call Group ID
- **Response 200**
  - `result` — string _(default=Success)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `GET` `/Dialplan/CallGroups/{id}/stat`

**Get queue info by ID**

Get information about the queue of a Call group

- operationId: `getQueueInfoById`
- **Scopes**: `callgroups:read`, `pbx:read`
- **Company API Key scope**: `callgroups:read`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — integer — Call group ID
    - `title` — string — Call group name
    - `totalMembers` — integer — Total number of members in the group
    - `loggedMembers` — integer — Number of logged-in users
    - `availableMembers` — integer — Number of available members in the group
    - `busyMembers` — integer — Number of calls in the queue
    - `waitingCalls` — integer — Number of calls waiting for an answer
- Errors: `401`, `403`, `404`

### Dictionary

#### `GET` `/Dictionaries`

**Get a list of dictionaries**

Returns the list of all available dictionaries on the PBX

- operationId: `pbxSettingsGetDialplansDictionary`
- **Scopes**: `info:read`, `pbx:read`
- **Company API Key scope**: `info:read`
- **Parameters**
  - `items` (query) — array — Returns a list of dictionaries given by an array
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `key` — string — Dictionary name
        - `items` — array
          - _array of_ `object`
            - `key` — string — Dialplan description
            - `value` — string — Dialplan description
  - `type` — string _(default=result)_
- Errors: `401`, `403`

### Dialplan DB

#### `POST` `/Dialplan/DB/{family}/{key}+/`

**Add a Dialplan Database value**

Adds a Dialplan Database value

- operationId: `addDialplanDb`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

#### `GET` `/Dialplan/DB/{family}/{key}+`

Get a Dialplan Database value

- operationId: `getDialplanDb`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=TestValue)_
- Errors: `400`, `401`, `500`

#### `GET` `/Dialplan/DB/{family}/`

**Get Dialplan Database family keys**

Returns Dialplan Database family keys

- operationId: `getFamilyKeys`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — string
    - `records` — array
      - _array of_ `object`
        - `key` — string
        - `value` — string
- Errors: `400`, `401`, `500`

#### `PUT` `/Dialplan/DB/{family}/{keys}+/`

**Update Dialplan Database value**

Update a Dialplan Database value

- operationId: `putDialplanDb`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

#### `DELETE` `/Dialplan/DB/{CustomFamily}/{testKey}+/`

Delete key and value from Dialplan Database

- operationId: `deleteDialplanDb`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

#### `DELETE` `/Dialplan/DB/{CustomFamily}/`

Delete all keys in family from Dialplan Database

- operationId: `deleteFamilyKeys`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `500`

### NTP

#### `GET` `/PBX/settings/ntp/`

**Get NTP settings**

Returns NTP server settings of the PBX.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `ntpGetSettings`
- **Response 200**
  - `result` — object
    - `pntp` — string — Primary NTP Server
    - `sntp` — string — Secondary NTP server
    - `time` — string — Time and date of the server, format 'dd/mm/yy HH:mm:ss'
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `PUT` `/PBX/settings/ntp/`

**Update NTP settings**

Updates NTP server settings for the PBX.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `ntpUpdateSettings`
- **Request body** (`application/json`)
  - `pntp` — string — Primary NTP Server (domain or IP)
  - `sntp` — string — Secondary NTP Server (domain or IP)
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

### HTTP Proxy

#### `GET` `/PBX/settings/httpProxy/`

**Get HTTP Proxy settings**

Returns HTTP Proxy server settings on the PBX.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `httpProxyGetSettings`
- **Response 200**
  - `result` — HttpProxyItem
    - `enable` — boolean — Enable HTTP proxy for Support VPN
    - `host` — string — Proxy host
    - `port` — string — Port
    - `auth_method` — string — Proxy authentication method _(default=none; enum: `none`, `basic`, `ntlm`)_
    - `login` — string — Login
    - `password` — string — Password
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `PUT` `/PBX/settings/httpProxy/`

**Update HTTP Proxy settings**

Updates HTTP Proxy server settings for the PBX.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `httpProxyUpdateSettings`
- **Request body** (`application/json`)
  - `enable` — boolean — Enable HTTP proxy for Support VPN
  - `host` — string **(required)** — Proxy host (required if 'enable' parameter is true)
  - `port` — string **(required)** — Port (required if 'enable' parameter is true)
  - `auth_method` — string — Proxy authentication method _(default=none; enum: `none`, `basic`, `ntlm`)_
  - `login` — string — Login
  - `password` — string — Password
- **Response 200**
  - `result` — HttpProxyItem
    - `enable` — boolean — Enable HTTP proxy for Support VPN
    - `host` — string — Proxy host
    - `port` — string — Port
    - `auth_method` — string — Proxy authentication method _(default=none; enum: `none`, `basic`, `ntlm`)_
    - `login` — string — Login
    - `password` — string — Password
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

### SMTP

#### `GET` `/PBX/settings/smtp/`

**Get SMTP settings**

Returns SMTP client options on the PBX.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `smtpGetOptions`
- **Scopes**: `smtp:read`, `pbx:read`
- **Company API Key scope**: `smtp:read`
- **Response 200**
  - `result` — SmtpItem
    - `account` — string — SMTP account _(default=default)_
    - `auth` — string — SMTP server auth type _(enum: `False`, `True`, `login`, `plain`, `cram-md5`, `digest-md5`, `gssapi`, `ntlm`)_
    - `host` — string — SMTP server host
    - `from` — string — From field in the email
    - `port` — integer — SMTP server port number
    - `timeout` — integer — SMTP server timeout for sending email _(enum: `2`, `5`, `10`, `15`, `20`, `60`)_
    - `user` — string — SMTP user name
    - `password` — string — SMTP user password
    - `domain` — string — HELO Domain
    - `tls` — boolean — Enable TLS for the secure connection
    - `tlsStartTls` — boolean — Enable STARTTLS to start TLS encryption
    - `isDefaultSettings` — boolean — Enable default SMTP settings (for Cloud PBX only)
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `PUT` `/PBX/settings/smtp/`

**Update SMTP options**

Update SMTP client options for PBX.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `smtpUpdateOptions`
- **Scopes**: `smtp:*`, `pbx:*`
- **Company API Key scope**: `smtp:*`
- **Request body** (`application/json`)
  - `account` — string — SMTP account _(default=default)_
  - `auth` — string **(required)** — SMTP server auth type _(enum: `False`, `True`, `login`, `plain`, `cram-md5`, `digest-md5`, `gssapi`, `ntlm`)_
  - `host` — string — SMTP server host (domain or IP)
  - `from` — string — From field in the email
  - `port` — integer **(required)** — SMTP server port number
  - `timeout` — integer **(required)** — SMTP server timeout for sending email _(enum: `2`, `5`, `10`, `15`, `20`, `60`)_
  - `user` — string — SMTP user name
  - `password` — string — SMTP user password
  - `domain` — string — HELO Domain
  - `tls` — boolean — Enable TLS for the secure connection
  - `tlsStartTls` — boolean — Enable STARTTLS to start TLS encryption
  - `isDefaultSettings` — boolean — Enable default SMTP settings (for Cloud PBX only)
- **Response 200**
  - `result` — SmtpItem
    - `account` — string — SMTP account _(default=default)_
    - `auth` — string — SMTP server auth type _(enum: `False`, `True`, `login`, `plain`, `cram-md5`, `digest-md5`, `gssapi`, `ntlm`)_
    - `host` — string — SMTP server host
    - `from` — string — From field in the email
    - `port` — integer — SMTP server port number
    - `timeout` — integer — SMTP server timeout for sending email _(enum: `2`, `5`, `10`, `15`, `20`, `60`)_
    - `user` — string — SMTP user name
    - `password` — string — SMTP user password
    - `domain` — string — HELO Domain
    - `tls` — boolean — Enable TLS for the secure connection
    - `tlsStartTls` — boolean — Enable STARTTLS to start TLS encryption
    - `isDefaultSettings` — boolean — Enable default SMTP settings (for Cloud PBX only)
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `POST` `/PBX/settings/smtp/test/`

**Run SMTP test**

Send test email with current SMTP options

- operationId: `smtpRunTest`
- **Scopes**: `smtp:*`, `pbx:*`
- **Company API Key scope**: `smtp:*`
- **Request body** (`application/json`) **(required)**
  - `mailto` — string **(required)** — Tested email
  - `from` — string **(required)** — From email
  - `body` — string **(required)** — Text of the email
- **Response 200**
  - `result` — object
    - `queued` — boolean — Queue runed
    - `testId` — string — Test name _(default=default)_
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `GET` `/PBX/settings/smtp/test/status/{testId}/`

**Get SMTP test status**

Returns SMTP test status

- operationId: `smtpGetTestStatus`
- **Scopes**: `smtp:read`, `pbx:read`
- **Company API Key scope**: `smtp:read`
- **Parameters**
  - `testId` (path) — string **(required)** — Test name _(default=default)_
- **Response 200**
  - `result` — object
    - `queued` — boolean — Queue runed
    - `testId` — string — Test name _(default=default)_
    - `content` — string — Log of SMTP server
  - `type` — string _(default=result)_
- Errors: `401`, `403`

### Sounds

#### `GET` `/Sounds/{path}/`

**Get Sounds**

Returns sounds

- operationId: `SoundsGet`
- **Scopes**: `sounds:read`, `pbx:read`
- **Company API Key scope**: `sounds:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `name` — string — Sound name.
        - `path` — string — Path to file or directory.
        - `size` — string — Filesize.
        - `isDir` — boolean — Is derectory.
        - `isDefault` — boolean — Is default sound or directory.
        - `modified` — integer — Last modified date(timestamp)
        - `formats` — array
          - _array of_ `object`
            - `type` — string — File type.
            - `path` — string — Link to download file.
  - `type` — string _(default=result)_
- Errors: `403`

#### `PUT` `/Sounds/{path}/`

**Edit Sound**

Lets to edit name or move sound files

- operationId: `SoundEdit`
- **Scopes**: `sounds:*`, `pbx:*`
- **Company API Key scope**: `sounds:*`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/Sounds/{path}/`

**Delete sound**

Allows to delete sound

- operationId: `SoundDelete`
- **Scopes**: `sounds:*`, `pbx:*`
- **Company API Key scope**: `sounds:*`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

#### `POST` `/Sounds/`

**Create sound**

Create or update sound

- operationId: `SoundsCreate`
- **Scopes**: `sounds:*`, `pbx:*`
- **Company API Key scope**: `sounds:*`
- **Request body** (`application/x-www-form-urlencoded`)
  - `file` — string — Sound file _(format=binary)_
  - `text` — string — Text to speech
  - `directory` — string — Target directory
  - `engine` — string — Language engine for TTS creation _(enum: `standard`, `neural`)_
  - `voice` — string — Voice
  - `volume` — integer — Speech volume
  - `speed` — integer — Speech speed
  - `pitch` — integer — Pitch
  - `filename` — string — Name of the speech file
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

#### `POST` `/Sounds/directory/`

**Create directory**

Create or update directory

- operationId: `DirectoryCreate`
- **Scopes**: `sounds:*`, `pbx:*`
- **Company API Key scope**: `sounds:*`
- **Request body** (`application/json`)
  - `path` — string — New path
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Sounds/directory/`

**Edit Directory**

Edit name or move directory.

- operationId: `Directorydit`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`

#### `DELETE` `/Sounds/directory/`

**Delete directory**

Delete directory.

- operationId: `DirectoryDelete`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`

### Upgrade

#### `GET` `/PBX/Upgrade/Settings/`

**Get upgrade settings**

Returns PBX upgrade settings.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `upgradeGetSettings`
- **Response 200**
  - `result` — UpgradeSettings
    - `wmsrelease` — object — WMS release section
      - `repository` — string — Upgrade repository _(default=rel50; enum: `rel50`, `rel50dev`, `rel50alpha`, `rel50beta`, `rel50test`)_
      - `enabled` — boolean — Enable PBX auto upgrade
      - `email` — string — Email for sending backup and upgrade log
      - `howly` — string — Interval for checking auto upgrade _(enum: `daily`, `weekly`, `monthly`)_
    - `customFirmwareServer` — object — Custom firmware server section
      - `url` — string — Custom firmware server URL (required if enabled)
      - `enabled` — boolean — Enable custom firmware server
      - `checkTls` — boolean — Check SSL/TLS Certificate for server
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `PUT` `/PBX/Upgrade/Settings/`

**Set upgrade settings**

****Available only for administrators with enabled ACL permissions to change settings****
<br>
> **You can save all sections (wmsrelease, customFirmwareServer) separately**

- operationId: `upgradeSetSettings`
- **Request body** (`application/json`) **(required)**
  - `wmsrelease[repository]` — string **(required)** — Upgrade repository _(default=rel50; enum: `rel50`, `rel50dev`, `rel50alpha`, `rel50beta`, `rel50test`)_
  - `wmsrelease[enabled]` — boolean **(required)** — Enable PBX auto upgrade
  - `wmsrelease[email]` — string **(required)** — Email for sending backup and upgrade log
  - `wmsrelease[howly]` — string **(required)** — Interval for checking auto upgrade _(enum: `daily`, `weekly`, `monthly`)_
  - `customFirmwareServer[url]` — string **(required)** — Custom firmware server URL (required if enabled)
  - `customFirmwareServer[enabled]` — boolean **(required)** — Enable custom firmware server
  - `customFirmwareServer[checkTls]` — boolean **(required)** — Check SSL/TLS Certificate for server
- **Response 200**
  - `result` — UpgradeSettings
    - `wmsrelease` — object — WMS release section
      - `repository` — string — Upgrade repository _(default=rel50; enum: `rel50`, `rel50dev`, `rel50alpha`, `rel50beta`, `rel50test`)_
      - `enabled` — boolean — Enable PBX auto upgrade
      - `email` — string — Email for sending backup and upgrade log
      - `howly` — string — Interval for checking auto upgrade _(enum: `daily`, `weekly`, `monthly`)_
    - `customFirmwareServer` — object — Custom firmware server section
      - `url` — string — Custom firmware server URL (required if enabled)
      - `enabled` — boolean — Enable custom firmware server
      - `checkTls` — boolean — Check SSL/TLS Certificate for server
  - `type` — string _(default=result)_
- Errors: `400`, `401`, `403`

#### `GET` `/PBX/Upgrade/Check/`

**Get result of the upgrade status**

Returns the result of the upgrade status.
**If the last check was started at least 3 minutes ago, a new check is forced to start**
****Available only for administrators with enabled ACL permissions to change settings.****

- operationId: `upgradeCheckGetStatus`
- **Response 200**
  - `result` — object
    - `repository` — string — Current upgrade repository
    - `newVersion` — string — New wms-interface version (if exists)
    - `newPackages` — boolean — Allowed new packages for upgrade
    - `check` — object — Checking info section
      - `isRunning` — boolean — Checking background process is running ##### **Need wait isRunning = false for get correct checking information**
      - `withoutError` — boolean — Checking finished without error
      - `fileSystemStatus` — boolean — Filesystem status is normal
      - `log` — array — Checking log
        - _array of_ `string`
    - `upgrade` — object — Upgrade info section
      - `isRunning` — boolean — Upgrade background process is running
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/PBX/Upgrade/Check/`

**Start the check**

Start checking upgrade script in the background.
****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `upgradeCheckStart`
- **Response 200**
  - `result` — object
    - `status` — boolean — Checking is started
    - `pid` — array — pid of running process
      - _array of_ `integer`
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `GET` `/PBX/Upgrade/`

**Get upgrade status**

****Available only for administrators with enabled ACL permissions to change settings****
Returns PBX upgrade status.
<br><br>
> If this script doesn’t return 200 Ok response, you can read the upgrade log from  /upgrade/wmsupgrade.out

- operationId: `upgradeGetStatus`
- **Response 200**
  - `result` — object
    - `isRunning` — boolean — Upgrade background process is running ##### **Need wait isRunning = false**
    - `completed` — boolean — Upgrade process is completed without error
    - `progress` — integer — Percent of upgrade
    - `log` — array — Upgrade log
      - _array of_ `string`
  - `type` — string _(default=result)_
- Errors: `401`, `403`, `500`

#### `POST` `/PBX/Upgrade/`

**Start upgrade**

****Available only for administrators with enabled ACL permissions to change settings****
<br>
**Steps to check new packages for the PBX**
- Run the check for new packages version: <a href="#operation/upgradeCheckStart">POST /PBX/Upgrade/Check/</a>
- Periodically call <a href="#operation/upgradeCheckGetStatus">GET /PBX/Upgrade/Check/</a> and wait till the check is completed.check.isRunning = false
- Check response, if the field newVersion is not empty or newPackages = true you nee to upgrade PBX.

<br>
**Steps to upgrade PBX**
- Run the upgrade of the PBX <a href="#operation/upgradeStart">POST /PBX/Upgrade/</a>
- Periodically call <a href="#operation/upgradeGetStatus">GET /PBX/Upgrade/</a> and wait till isRunning = false
- After the upgrade is finished, reboot the PBX: <a href="#operation/systemReboot">PUT /PBX/System/Reboot/</a>

- operationId: `upgradeStart`
- **Response 200**
  - `result` — object
    - `status` — boolean — Started new upgrade process in background _(default=True)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

### System

#### `PUT` `/PBX/System/Reboot/`

**Start PBX reboot**

****Available only for administrators with enabled ACL permissions to change settings****

- operationId: `systemReboot`
- **Scopes**: `pbxpower:*`, `pbx:*`
- **Company API Key scope**: `pbxpower:*`
- **Response 200**
  - `result` — string _(default=Done)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

### Calls

#### `POST` `/Calls/`

**Make a new call**

Make a new call with a user

- operationId: `postCall`
- **Request body** (`application/json`) **(required)**
  - `number` — string **(required)** — Called number
  - `name` — string — User name _(default=number)_
  - `device` — string — Device type _(default=any_device)_
- **Response 200** (`ApiResponseTrue`)
  - `type` — string _(enum: `result`)_
  - `result` — boolean _(enum: `True`)_
- Errors: `400`, `401`, `403`, `500`

#### `POST` `/Calls/{channel}/Dtmf`

**Send DTMF**

Send DTMF to channel

- operationId: `postCallDtmf`
- **Parameters**
  - `channel` (path) — string **(required)** — SIP channel (URL-encoded)
- **Request body** (`application/json`) **(required)**
  - `dtmf` — string **(required)** — DTMF code _(enum: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, `#`)_
  - `sendOnBridgedChannel` — string — Send DTMF code to current or bridged channel _(default=True; enum: `True`, `False`)_
- **Response 200** (`ApiResponseTrue`)
  - `type` — string _(enum: `result`)_
  - `result` — boolean _(enum: `True`)_
- Errors: `400`, `401`, `403`, `500`

#### `GET` `/Calls/{channel}`

Get call status

- operationId: `getCallStatus`
- **Parameters**
  - `channel` (path) — string **(required)** — SIP channel (URL-encoded)
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `Accountcode` — string
    - `BridgedChannel` — string
    - `BridgedUniqueid` — string
    - `CallerIDName` — string
    - `CallerIDNum` — string
    - `Channel` — string
    - `ChannelState` — string
    - `ChannelStateDesc` — string
    - `ConnectedLineName` — string
    - `ConnectedLineNum` — string
    - `Context` — string
    - `Extension` — string
    - `Priority` — string
    - `Privilege` — string
    - `Seconds` — string
    - `Uniqueid` — string
- Errors: `400`, `401`, `403`, `500`

#### `GET` `/Calls/{channel}/Recordings`

Get call recordings

- operationId: `getCallRecordings`
- **Parameters**
  - `channel` (path) — string **(required)** — SIP channel (URL-encoded)
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — string
    - `records` — array
      - _array of_ `object`
        - `date` — string
        - `destination` — string
        - `file` — string
        - `source` — string
- Errors: `400`, `401`, `403`, `500`

#### `GET` `/Calls/{channel}/Tags`

Get call tags

- operationId: `getCallTags`
- **Parameters**
  - `channel` (path) — string **(required)** — SIP channel (URL-encoded)
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=tag1,tag2)_
- Errors: `400`, `401`, `403`, `500`

#### `PUT` `/Calls/{channel}/Tags`

Set call tags

- operationId: `setTagsToCall`
- **Parameters**
  - `channel` (path) — string **(required)** — SIP channel (URL-encoded)
  - `tags` (path) — string **(required)** — The value of tags.
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`, `500`

#### `POST` `/Calls/{channel}/Transfer`

Call transfer

- operationId: `transferToCall`
- **Parameters**
  - `channel` (path) — string **(required)** — SIP channel (URL-encoded)
- **Request body** (`application/json`) **(required)**
  - `to` — string **(required)** — Number or channel
  - `type` — string — Redirect or Bridge
  - `context` — string — Only for type redirect
  - `priority` — string — Only for type redirect
- **Response 200** (`ApiResponseTrue`)
  - `type` — string _(enum: `result`)_
  - `result` — boolean _(enum: `True`)_
- Errors: `400`, `401`, `403`, `500`

### Contacts

#### `GET` `/Contacts/`

Get contacts

- operationId: `getContacts`
- **Scopes**: `phonebooks:read`, `pbx:read`
- **Company API Key scope**: `phonebooks:read`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. _(default=All)_
  - `start` (query) — string — Offset rows returned _(default=0)_
  - `count` (query) — string — How many rows to return _(default=100)_
  - `sort` (query) — string — Sort field _(default=name)_
  - `dir` (query) — string — Type of sorting _(default=ASC)_
  - `search` (query) — string — Search words If search fields are not specified, search is performed by the following fields: name email extension phone fax mobile organization
  - `searchFields` (query) — string — Field to be searched, there may be several fields. You can use commas "," to list all required fields. _(default=name)_
  - `filter[$key]` (query) — string — When filtering by any field, you can also use range [from][to] _(default=empty)_
- **Response 200** (`list2`)
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — int _(default=112)_
    - `records` — array
      - _array of_ `object`
        - `id` — int
        - `email` — string
        - `extension` — string
        - `phone` — string
        - `office` — string
        - `home` — string
        - `home_mobile` — string
        - `fax` — string
        - `mobile` — string
        - `organization` — string
        - `picture` — string
        - `shortcut` — string
        - `phonebook_id` — int
        - `type` — string
        - `note` — string
        - `address` — string
        - `vat_id` — string
        - `name_prefix` — string
        - `document_type` — string
        - `document_id` — string
        - `pin` — string
        - `credit` — string
        - `hash` — string
        - `country` — string
        - `date_birth` — string
        - `born_in` — string
        - `postal_code` — string
        - `city` — string
        - `province` — string
        - `license_plate` — string
        - `document_released` — string
        - `document_from` — string
        - `department` — string
        - `last_update` — string
- Errors: `401`, `403`, `500`

#### `GET` `/Contacts/{contactIds}/`

**Get a contact by ID**

Returns a contact by ID

- operationId: `getContactsById`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. _(default=All)_
- **Response 200** (`listContactsId`)
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — int
    - `email` — string
    - `extension` — string
    - `phone` — string
    - `office` — string
    - `home` — string
    - `home_mobile` — string
    - `fax` — string
    - `mobile` — string
    - `organization` — string
    - `picture` — string
    - `shortcut` — string
    - `phonebook_id` — int
    - `type` — string
    - `note` — string
    - `address` — string
    - `vat_id` — string
    - `name_prefix` — string
    - `document_type` — string
    - `document_id` — string
    - `pin` — string
    - `credit` — string
    - `hash` — string
    - `country` — string
    - `date_birth` — string
    - `born_in` — string
    - `postal_code` — string
    - `city` — string
    - `province` — string
    - `license_plate` — string
    - `document_released` — string
    - `document_from` — string
    - `department` — string
    - `last_update` — string
- Errors: `401`, `500`

#### `DELETE` `/Contacts/{id}/`

**Delete a contact**

****Available only for administrators****

- operationId: `delContacts`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `contacts` — int _(default=1)_
- Errors: `401`

#### `PUT` `/Contacts/{id}`

Update a contact

- operationId: `updateContacts`
- **Parameters**
  - `data` (query) — array **(required)**
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `changed` — int _(default=1)_
- Errors: `401`, `500`

#### `POST` `/Contacts`

Add a contact

- operationId: `postContacts`
- **Scopes**: `phonebooks:*`, `pbx:*`
- **Company API Key scope**: `phonebooks:*`
- **Parameters**
  - `data` (query) — array **(required)** — Required parameters: name, phonebook_id
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — int _(default=58466)_
- Errors: `401`, `403`, `500`

#### `DELETE` `/Phonebooks/{id}/Contacts/`

Delete contacts in a phonebook

- operationId: `delPhonebooksContacts`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `contacts` — int _(default=1)_
- Errors: `401`

#### `GET` `/Phonebooks/{phonebookID}/Contacts/`

Get contacts from a phonebook

- operationId: `getPhonebooksContacts`
- **Scopes**: `phonebooks:read`, `pbx:read`
- **Company API Key scope**: `phonebooks:read`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. _(default=All)_
  - `start` (query) — string — Offset rows returned _(default=0)_
  - `count` (query) — string — How many rows to return _(default=100)_
  - `sort` (query) — string — Sort field _(default=name)_
  - `dir` (query) — string — Type of sorting _(default=ASC)_
  - `search` (query) — string — Search words If search fields are not specified, search is performed by the following fields: name email extension phone fax mobile organization
  - `searchFields` (query) — string — Field to be searched, there may be several fields. You can use commas "," to list all required fields. _(default=name)_
  - `filter[$key]` (query) — string — When filtering by any field, you can also use range [from][to] _(default=empty)_
- **Response 200** (`list2`)
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — int _(default=112)_
    - `records` — array
      - _array of_ `object`
        - `id` — int
        - `email` — string
        - `extension` — string
        - `phone` — string
        - `office` — string
        - `home` — string
        - `home_mobile` — string
        - `fax` — string
        - `mobile` — string
        - `organization` — string
        - `picture` — string
        - `shortcut` — string
        - `phonebook_id` — int
        - `type` — string
        - `note` — string
        - `address` — string
        - `vat_id` — string
        - `name_prefix` — string
        - `document_type` — string
        - `document_id` — string
        - `pin` — string
        - `credit` — string
        - `hash` — string
        - `country` — string
        - `date_birth` — string
        - `born_in` — string
        - `postal_code` — string
        - `city` — string
        - `province` — string
        - `license_plate` — string
        - `document_released` — string
        - `document_from` — string
        - `department` — string
        - `last_update` — string
- Errors: `401`, `403`, `500`

#### `DELETE` `/Phonebooks/{phonebookID}/Contacts/{contactId}/`

Delete a contact

- operationId: `delPhonebooksToContacts`
- **Scopes**: `phonebooks:*`, `pbx:*`
- **Company API Key scope**: `phonebooks:*`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `contacts` — int _(default=1)_
- Errors: `401`, `403`

#### `GET` `/Phonebooks/{phonebookID}/Contacts/{contactId}`

Get a contact from phonebook

- operationId: `getPhonebooksContactsId`
- **Scopes**: `phonebooks:read`, `pbx:read`
- **Company API Key scope**: `phonebooks:read`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. _(default=All)_
- **Response 200** (`listContactsId`)
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — int
    - `email` — string
    - `extension` — string
    - `phone` — string
    - `office` — string
    - `home` — string
    - `home_mobile` — string
    - `fax` — string
    - `mobile` — string
    - `organization` — string
    - `picture` — string
    - `shortcut` — string
    - `phonebook_id` — int
    - `type` — string
    - `note` — string
    - `address` — string
    - `vat_id` — string
    - `name_prefix` — string
    - `document_type` — string
    - `document_id` — string
    - `pin` — string
    - `credit` — string
    - `hash` — string
    - `country` — string
    - `date_birth` — string
    - `born_in` — string
    - `postal_code` — string
    - `city` — string
    - `province` — string
    - `license_plate` — string
    - `document_released` — string
    - `document_from` — string
    - `department` — string
    - `last_update` — string
- Errors: `401`, `403`, `500`

#### `PUT` `/phonebooks/{phonebookID}/Contacts/{contactId}`

Update a phonebook

- operationId: `updatePhonebooksContacts`
- **Scopes**: `phonebooks:*`, `pbx:*`
- **Company API Key scope**: `phonebooks:*`
- **Parameters**
  - `data` (query) — array **(required)**
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `changed` — int _(default=1)_
- Errors: `401`, `403`, `500`

#### `POST` `/Phonebooks/{phonebookID}/Contacts`

Add a contact from Phonebooks

- operationId: `addPhonebooksContacts`
- **Scopes**: `phonebooks:*`, `pbx:*`
- **Company API Key scope**: `phonebooks:*`
- **Parameters**
  - `data` (query) — array **(required)** — Required parameters: name
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — int _(default=58466)_
- Errors: `401`, `403`, `500`

### iOS

#### `GET` `/iOS/Config/`

Get an iOS config

- operationId: `getConfig`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. _(default=groups colleagues personalInfo dialplanSettings pbxInfo wideband sip-rtp cdrSettings personalSettings pagingGroups conference env)_
  - `filter` (query) — string — Each of the four filter groups should have relevant ACL permissions to perform the request. Separated by comma ","
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `groups` — array
      - _array of_ `object`
        - `dn` — string
        - `id` — string
        - `name` — string
        - `wcgrp` — string
    - `colleagues` — array
      - _array of_ `object`
        - `dn` — string
        - `id` — string
        - `name` — string
        - `login` — string
        - `extension` — string
        - `officePhone` — string
        - `mobilePhone` — string
        - `faxNumber` — string
        - `email` — string
        - `pbxDn` — string
        - `role` — string
        - `groupDn` — string
        - `language` — string
        - `dialplan` — string
        - `faxDialplan` — string
        - `department` — string
        - `picture` — string
        - `sourceId` — string
        - `licenseType` — string
        - `jid` — string
    - `personalInfo` — object
      - `dn` — string
      - `id` — string
      - `name` — string
      - `extension` — string
      - `officePhone` — string
      - `mobilePhone` — string
      - `faxNumber` — string
      - `email` — string
      - `pbxDn` — string
      - `role` — string
      - `language` — string
      - `dialplan` — string
      - `faxDialplan` — string
      - `departament` — string
      - `sipPassword` — string
    - `personalSettings` — object
      - `personal` — object
        - `email` — string
        - `mobilePhone` — string
      - `ringtones` — object
        - `Emergency` — array
          - _array of_ `any`
        - `External` — array
          - _array of_ `any`
        - `Ring1` — array
          - _array of_ `any`
        - `Ring2` — array
          - _array of_ `any`
        - `Ring3` — array
          - _array of_ `any`
        - `Ring4` — array
          - _array of_ `any`
        - `Ring5` — array
          - _array of_ `any`
        - `backwards` — array
          - _array of_ `any`
        - `elevator` — array
          - _array of_ `any`
        - `guitar1` — array
          - _array of_ `any`
        - `harp1` — array
          - _array of_ `any`
        - `harp2` — array
          - _array of_ `any`
        - `piano1` — array
          - _array of_ `any`
        - `piano2` — array
          - _array of_ `any`
        - `piano3` — array
          - _array of_ `any`
        - `piano4` — array
          - _array of_ `any`
        - `piano5` — array
          - _array of_ `any`
        - `rhodes` — array
          - _array of_ `any`
        - `silent` — array
          - _array of_ `any`
        - `soul` — array
          - _array of_ `any`
        - `wurlitzer` — array
          - _array of_ `any`
      - `fkeys` — object
        - `keys` — array
          - _array of_ `object`
            - `key` — string
            - `value` — string
            - `title` — string
        - `list` — object
          - `STIME` — array
            - _array of_ `any`
          - `TRUNK` — array
            - _array of_ `any`
          - `SWITCH` — array
            - _array of_ `any`
          - `3SWITCH` — array
            - _array of_ `any`
          - `GPICKUP` — object
            - `1` — string
            - `2` — string
            - `3` — string
          - `QPICKUP` — object
            - `1` — string
            - `2` — string
            - `3` — string
            - `4` — string
            - `5` — string
          - `QCALL` — object
            - `1` — string
            - `2` — string
            - `3` — string
            - `4` — string
            - `5` — string
      - `features` — object
        - `internal` — object
          - `away` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `dnd` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `default` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `external` — object
          - `away` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `dnd` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `default` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `blacklist` — object
          - `away` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `dnd` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `default` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `whitelist` — object
          - `away` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `dnd` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `default` — object
            - `_ACTIVATED` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MEXT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `BCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `UCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `SMSMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `REJECT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `EMAILMCN` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `FCF` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `TOUT` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `CW` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `MOBCONFIRMATION` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
            - `RING` — object
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `sharedvm` — object
        - `status` — string
        - `value` — string
      - `cwtone` — object
        - `status` — string
    - `pagingGroups` — object
      - `total` — int
      - `records` — array
        - _array of_ `any`
    - `dialplanSettings` — object
      - `transferdigittimeout` — string
      - `transferinterdigittimeout` — string
      - `GEOD` — string
      - `featureCodes` — object
        - `preferences` — object
          - `PREFIX` — string
        - `services` — object
          - `VMACCESS` — string
          - `DIRECTORY` — string
          - `LOGIN` — string
          - `PERSONALRECORD` — string
          - `PBXRECORD` — string
          - `SBARGE` — string
          - `PBARGE` — string
          - `CBARGE` — string
          - `SENDDOC` — string
          - `FAXRELAY` — string
          - `PAGING` — string
          - `HIDECID` — string
          - `SWITCH` — string
          - `3SWITCH` — string
          - `STIME` — string
          - `PICKUP` — string
          - `CONTINUITYCALL` — string
          - `QCALL` — string
          - `CGMANAGER` — string
          - `INTERCOM` — string
          - `SHORTNUM` — string
          - `CONFERENCE` — string
          - `ECHO` — string
          - `WHOTELALARM` — string
          - `WHOTELMUR` — string
          - `IDENTITY` — string
          - `WHOTELINSPECT` — string
          - `WHOTELBAR` — string
    - `cdrSettings` — object
      - `save_chat_history` — boolean
    - `pbxInfo` — object
      - `networkAddresses` — array
        - _array of_ `any`
      - `ports` — array
        - _array of_ `any`
      - `externalLinePrefix` — string
      - `version` — string
      - `serial` — string
      - `country` — object
        - `iso` — string
        - `name` — string
        - `code` — int
    - `wideband` — boolean
    - `sip-rtp` — object
      - `jitter` — object
        - `min` — string
        - `average` — string
        - `max` — string
      - `DSCP` — object
        - `RTP` — int
        - `SIP` — int
    - `conference` — object
      - `groupChatDomain` — string
      - `smsBotDomain` — string
    - `env` — object
      - `ECHO_CANCELLATION` — string
      - `NOISE_SUPPRESSION` — string
      - `COLLABORATION_COLLEAGUES_CHUNK_LIMIT` — integer
      - `CALL_CONTROL_FEATURE` — boolean
- Errors: `401`, `500`

### Video Conference

#### `GET` `/videoConference/Rooms/`

**Get rooms**

Get the rooms in which the user is a participant

- operationId: `getRooms`
- **Response 200**
  - `result` — array
    - _array of_ `getRoom`
      - `room` — string — Room ID
      - `pin` — string — Conference ID number. Required to connect to a conference with Dial numbers
      - `jid` — string — Room JID
      - `url` — string — Conference URL
      - `subject` — string — Room title
      - `owner` — string — Owner JID
      - `created` — integer — Timestamp when the room was created
      - `visited` — integer — Timestamp when the room was visited
      - `online` — boolean — Whether the conference is active
      - `occupants` — integer — The number of users who are currently in the conference
      - `schedule` — object — Conference schedule
        - `start` — string — Conference start date and time
        - `end` — string — Conference end date and time
        - `recurrence` — string — Conference frequency. String in RRULE RFC 5454
        - `description` — string — Conference description
        - `enabled` — boolean — Enable or disable the schedule
        - `country` — string — Two-letter ISO 3166 country code
        - `timezone` — string — The IANA time zone identifier
        - `lang` — string — Two-letter language code
        - `dialInNumbers` — array — Two-letter country codes for connecting to a phone conference in these countries.
          - _array of_ `string`
      - `participants` — object — Conference participants
        - `type` — string — Type of a participant. Colleague or email invitee
        - `name` — string — Participant name
        - `jid` — string — Participant JID
        - `email` — string — Participant email
        - `phone` — string — Participant phone
        - `extension` — string — Participant extension
        - `serial` — string — PBX serial
      - `password` — string — Conference password
      - `passwordPin` — string — Conference password for HW
  - `type` — string _(format=result)_
- Errors: `401`

#### `POST` `/videoConference/Rooms/`

**Create a room**

Create a new room
****Available for users with enabled ACL permissions - create conferences and the user needs a business, premium or wizyconf license****

- operationId: `postRoom`
- **Response 200**
  - `result` — getRoom
    - `room` — string — Room ID
    - `pin` — string — Conference ID number. Required to connect to a conference with Dial numbers
    - `jid` — string — Room JID
    - `url` — string — Conference URL
    - `subject` — string — Room title
    - `owner` — string — Owner JID
    - `created` — integer — Timestamp when the room was created
    - `visited` — integer — Timestamp when the room was visited
    - `online` — boolean — Whether the conference is active
    - `occupants` — integer — The number of users who are currently in the conference
    - `schedule` — object — Conference schedule
      - `start` — string — Conference start date and time
      - `end` — string — Conference end date and time
      - `recurrence` — string — Conference frequency. String in RRULE RFC 5454
      - `description` — string — Conference description
      - `enabled` — boolean — Enable or disable the schedule
      - `country` — string — Two-letter ISO 3166 country code
      - `timezone` — string — The IANA time zone identifier
      - `lang` — string — Two-letter language code
      - `dialInNumbers` — array — Two-letter country codes for connecting to a phone conference in these countries.
        - _array of_ `string`
    - `participants` — object — Conference participants
      - `type` — string — Type of a participant. Colleague or email invitee
      - `name` — string — Participant name
      - `jid` — string — Participant JID
      - `email` — string — Participant email
      - `phone` — string — Participant phone
      - `extension` — string — Participant extension
      - `serial` — string — PBX serial
    - `password` — string — Conference password
    - `passwordPin` — string — Conference password for HW
  - `type` — string _(format=result)_
- Errors: `401`, `403`

#### `PUT` `/videoConference/Rooms/`

**Update the room**

Update the room
****Only the participant can update the room****

- operationId: `putRoom`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `403`

#### `DELETE` `/videoConference/Rooms/`

**Delete the room**

Delete the room
****If the user isn't the owner of the room, the room will not be deleted, and the user will leave it****

- operationId: `deleteRoom`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `403`

#### `POST` `/videoConference/invite/`

Invite user to conference

- operationId: `videoConferenceInvite`
- **Request body** (`application/json`) **(required)**
  - `payload` — object **(required)** — payload={"name":"u300 Conference","room":5682708,"join":true,"reinvite":true,"users":[{"name":"Eric Cartman","payload":{"name":"Eric Cartman","jid":"10@wildix","value":"10@wildix"}}]}
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `room` — string _(default=5682708)_
    - `pbxHost` — string _(default=pbx080c295a2942.wildixin.com)_
    - `externalUrl` — string _(default=https:\/\/conference.wildix.com\/conf\/5682708)_
- Errors: `401`, `500`

### Originate

#### `GET` `/originate/AlarmClocks/{id}/`

Get an alarm clock

- operationId: `getAlarmClocks`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — string _(default=105851541)_
    - `postpone` — string _(default=26/01/2015 08:10)_
    - `number` — string _(default=105)_
- Errors: `401`, `500`

#### `POST` `/originate/AlarmClocks/`

Make an alarm clock

- operationId: `addAlarmClocks`
- **Request body** (`application/json`) **(required)**
  - `number` — int **(required)** — The phone number.
  - `postpone` — string — Date of sending the delayed message.
  - `dialplan` — string — The dialplan name. _(default=alarmclock)_
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=105851541)_
- Errors: `400`, `401`, `500`

#### `DELETE` `/originate/AlarmClocks/{id}`

Remove an alarm clock

- operationId: `deleteAlarmClocks`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

#### `POST` `/Originate/`

Make an originate request

- operationId: `addOriginate`
- **Request body** (`application/json`) **(required)**
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
  - `async` — string — true or false.
  - `actionid` — string
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `500`

#### `POST` `/Originate/Call/`

Make a call

- operationId: `addOriginateCall`
- **Request body** (`application/json`) **(required)**
  - `number` — string **(required)** — The phone number.
  - `postpone` — string — Date of sending the delayed message.
  - `name` — string — The name.
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `500`

#### `POST` `/Originate/mobility/`

Make a mobility call

- operationId: `addOriginateMobility`
- **Request body** (`application/json`) **(required)**
  - `number` — string **(required)** — The phone number.
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `500`

#### `POST` `/Originate/sms/`

Send an SMS

- operationId: `addOriginateSms`
- **Request body** (`application/json`) **(required)**
  - `number` — string — The phone number or several numbers separated by commas. Example: +391234567890 or +391234567890,+391234567891,+391234567892,...
  - `message` — string — The body of SMS messages, maximum length is 300 characters.
  - `disableHeaderMessage` — boolean — Disable header message
  - `postpone` — string — Date of sending the delayed message. Example: 14/07/2014 15:35
  - `gsm` — string — GSM gateway MAC address. Example: 9c7514330001
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `500`

### Smart Notifications

#### `POST` `/notifications/`

**Add a new smart notification**

Add either a Regular Notification or a Private Notification

- operationId: `addSmartNotification`
- **Request body** (`application/json`) **(required)**
  - _oneOf_ — exactly one of:
    - **`Regular Notification`**
      - `from` — string **(required)** — Source of the notification.
      - `notificationType` — string **(required)** — Type of the regular notification. _(enum: `BroadcastMessage`, `Call`, `VideoCall`)_
      - `event` — string **(required)** — Description of the event.
      - `broadcastMessage` — string **(required)** — The message for announcement.
      - `broadcastId` — string **(required)** — The broadcast ID to which the notification will be sent.
      - `playFrequency` — integer — How often (each N seconds) the request should repeat. _(default=10; min=5; max=30)_
      - `confirmationTimeout` — integer — Timeout (in seconds) for confirmation. _(default=30; min=0; max=600)_
      - `queueTimeout` — integer — Timeout (in seconds) for queue processing. _(default=60; min=5; max=600)_
      - `origin` — string — Source of the request.
      - `priority` — integer — Priority of the notification. _(default=0; min=0)_
      - `customRid` — string — Custom request ID.
      - `skipTranscribe` — boolean — Skip notification transcribing
      - `skills` — array — Optional list of skill names (LDAP department names) to filter notification recipients within the broadcast. Empty or absent array means no filtering — message plays to all subscribers in the broadcast.
        - _array of_ `string`
    - **`Private Notification`**
      - `from` — string **(required)** — Source of the notification.
      - `notificationType` — string **(required)** — Type of the private notification. _(enum: `PrivateMessage`)_
      - `event` — string **(required)** — Description of the event.
      - `broadcastMessage` — string **(required)** — The message for announcement.
      - `extension` — string **(required)** — User extension number to receive the Private Message.
      - `origin` — string — Source of the request.
      - `customRid` — string — Custom request ID.
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `requestId` — string
- Errors: `400`, `401`, `403`, `500`

### Groups

#### `GET` `/Groups/`

Get user groups

- operationId: `getGroups`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — array
    - _array of_ `object`
      - `dn` — string
      - `id` — string
      - `name` — string
      - `wcgrp` — string
- Errors: `401`, `500`

### Fax

#### `POST` `/fax/`

Send the fax

- operationId: `addFax`
- **Request body** (`application/json`) **(required)**
  - `faxNumbers` — array **(required)** — Extensions from which the fax will be send
    - _array of_ `any`
  - `fileName` — array **(required)** — name of the uploaded file or file
    - _array of_ `any`
  - `postpone` — boolean
  - `faxCover` — boolean
  - `faxCoverTo` — string
  - `faxCoverToPhone` — string
  - `faxCoverToCompany` — string
  - `faxCoverFrom` — string
  - `faxCoverFromPhone` — string
  - `faxCoverFromCompany` — string
  - `faxCoverSubject` — string
  - `faxCoverNotes` — string
  - `faxCoverFromFax` — string
  - `faxCoverCheckboxUrgent` — boolean
  - `faxCoverCheckboxReview` — boolean
  - `faxCoverCheckboxComment` — boolean
  - `faxCoverCheckboxReply` — boolean
  - `faxCoverCheckboxForward` — boolean
  - `postponeDate` — string
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `status` — string _(default=success)_
    - `fileExists` — boolean _(default=True)_
- Errors: `401`, `500`

#### `POST` `/fax/file/`

**Upload file to be send via fax**

Upload the file that should be send via fax

- operationId: `addFile`
- **Request body** (`application/x-www-form-urlencoded`) **(required)**
  - `qqfile` — string **(required)** — file in format PDF or TIFF _(format=binary)_
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=example.tiff)_
- Errors: `400`, `401`, `500`

### User

#### `GET` `/User/{extension}/Presence/`

**Get user presence**

Returns user presence

- operationId: `getUser`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `online` — boolean _(default=True)_
    - `show` — string _(default=away)_
    - `until` — string _(default=2015-03-27 10:08:00+00:00)_
    - `device_show` — string _(default=talking)_
    - `status` — string _(default=Meeting)_
    - `location` — object
      - `address` — string _(default=Località le Basse, 11, 38123 Trento, Italy)_
      - `lat` — string _(default=46)_
      - `lng` — string _(default=11.1261)_
- Errors: `401`, `500`

#### `PUT` `/User/{extension}/Presence`

Update user presence

- operationId: `updateUser`
- **Request body** (`application/json`) **(required)**
  - `status` — string **(required)** — Possible values: available away dnd mur
  - `message` — string _(default=empty)_
  - `until` — string — Format: "19/09/2017 11:30" in UTC _(default=empty)_
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

### Phonebooks

#### `GET` `/Phonebooks/`

Get phonebooks

- operationId: `getPhonebooks`
- **Scopes**: `phonebooks:read`, `pbx:read`
- **Company API Key scope**: `phonebooks:read`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. sync_params - only for admins _(default=All)_
  - `start` (query) — string — Offset rows returned _(default=0)_
  - `count` (query) — string — How many rows to return _(default=100)_
  - `sort` (query) — string — Sort field _(default=name)_
  - `dir` (query) — string — Type of sorting _(default=ASC)_
  - `search` (query) — string — Search words If search fields are not specified, search is performed by the following fields: name
  - `searchFields` (query) — string — Field to be searched, there may be several fields. You can use commas "," to list all required fields. _(default=name)_
  - `filter[$key]` (query) — string — When filtering by any field, you can also use range [from][to] _(default=empty)_
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — int _(default=6)_
    - `records` — array
      - _array of_ `object`
        - `id` — int
        - `name` — string
        - `type` — int
        - `hash` — string
        - `owner_id` — int
        - `sync_set` — int
        - `sync_interval` — int
- Errors: `401`, `403`, `500`

#### `GET` `/Phonebooks/{id}/`

Get a phonebook

- operationId: `getPhonebooksId`
- **Scopes**: `phonebooks:read`, `pbx:read`
- **Company API Key scope**: `phonebooks:read`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. sync_params - only for admins _(default=All)_
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — int
    - `name` — string
    - `type` — int
    - `hash` — string
    - `owner_id` — int
    - `sync_set` — int
    - `sync_interval` — int
- Errors: `401`, `403`, `500`

#### `POST` `/Phonebooks`

Add a phonebook

- operationId: `addPhonebook`
- **Scopes**: `phonebooks:*`, `pbx:*`
- **Company API Key scope**: `phonebooks:*`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — int
- Errors: `401`, `403`, `500`

#### `PUT` `/Phonebooks/{id}`

Update a phonebook

- operationId: `updatePhonebook`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `changed` — int
- Errors: `401`, `500`

#### `DELETE` `/Phonebooks/{PhonebookId}/`

Delete a phonebook

- operationId: `deletePhonebook`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `phonebooks` — int
    - `contacts` — int
- Errors: `401`, `500`

### Personal

#### `GET` `/Personal/Acl/`

Get ACL options

- operationId: `getAcl`
- **Parameters**
  - `filter` (query) — array **(required)** — Each of the four filter groups should have relevant ACL permissions to perform the request. Separated by comma "," Note: filter param should be an array which contains key, one of four possible values and value must be an ACL list. Possible values: yesno, canuse, canset, cancall
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `acl` — object
      - `yesno` — object
        - `CHANGE_PRESENCE` — object
          - `gid=1620516345,o=com0,dc=wildix` — boolean _(default=False)_
          - `gid=1711417694,o=com0,dc=wildix` — boolean _(default=True)_
          - `gid=6777911,o=com0,dc=wildix` — boolean _(default=False)_
          - `gid=4873662,o=com0,dc=wildix` — boolean _(default=True)_
        - `SEE_CALLS` — object
          - `gid=1620516345,o=com0,dc=wildix` — boolean _(default=True)_
          - `gid=1711417694,o=com0,dc=wildix` — boolean _(default=True)_
          - `gid=6777911,o=com0,dc=wildix` — boolean _(default=True)_
          - `gid=4873662,o=com0,dc=wildix` — boolean _(default=True)_
- Errors: `400`, `401`, `500`

#### `GET` `/Personal/Info/`

Get personal info

- operationId: `getInfo`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. You can use commas to list all required fields. Possible values: dn id name extension officePhone mobilePhone faxNumber email pbxDn role groupDn language login picture dialplan faxDialplan department sipPassword _(default=All)_
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `dn` — string _(default=uid=299253131,o=com0,dc=wildix)_
    - `id` — string _(default=299253131)_
    - `name` — string _(default=admin)_
    - `extension` — string _(default=)_
    - `officePhone` — string _(default=)_
    - `mobilePhone` — string _(default=)_
    - `faxNumber` — string _(default=)_
    - `email` — string _(default=)_
    - `pbxDn` — string _(default=pbxid=221100001aa3,dc=wildix)_
    - `role` — string _(default=admin)_
    - `groupDn` — string _(default=gid=1192724752,o=com0,dc=wildix)_
    - `language` — string _(default=en)_
    - `dialplan` — string _(default=internalcalls)_
    - `faxDialplan` — string _(default=internalcalls)_
    - `department` — string _(default=)_
    - `picture` — string _(default=)_
    - `sourceId` — string _(default=)_
    - `licenseType` — string _(default=premium)_
    - `jid` — string _(default=@krzhevitskywms4.wildixin.com)_
    - `sipPassword` — string _(default=sipPassword)_
- Errors: `401`, `500`

#### `GET` `/Personal/settings/`

Get settings

- operationId: `getSettings`
- **Parameters**
  - `fields` (query) — string — A list of fields that should be returned. Items of the list can be separated by commas ",". _(default=All; enum: `features`, `fkeys`, `personal`, `ringtones`, `sharedvm`, `cwtone`, `contactCenter`, `popupUrl`)_
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `personal` — object
      - `email` — string
      - `mobilePhone` — string
    - `ringtones` — object
      - `Emergency` — array
        - _array of_ `any`
      - `External` — array
        - _array of_ `any`
      - `Ring1` — array
        - _array of_ `any`
      - `Ring2` — array
        - _array of_ `any`
      - `Ring3` — array
        - _array of_ `any`
      - `Ring4` — array
        - _array of_ `any`
      - `Ring5` — array
        - _array of_ `any`
      - `backwards` — array
        - _array of_ `any`
      - `elevator` — array
        - _array of_ `any`
      - `guitar1` — array
        - _array of_ `any`
      - `harp1` — array
        - _array of_ `any`
      - `harp2` — array
        - _array of_ `any`
      - `piano1` — array
        - _array of_ `any`
      - `piano2` — array
        - _array of_ `any`
      - `piano3` — array
        - _array of_ `any`
      - `piano4` — array
        - _array of_ `any`
      - `piano5` — array
        - _array of_ `any`
      - `rhodes` — array
        - _array of_ `any`
      - `silent` — array
        - _array of_ `any`
      - `soul` — array
        - _array of_ `any`
      - `wurlitzer` — array
        - _array of_ `any`
    - `fkeys` — object
      - `keys` — array
        - _array of_ `object`
          - `key` — string
          - `value` — string
          - `title` — string
      - `list` — object
        - `STIME` — array
          - _array of_ `any`
        - `TRUNK` — array
          - _array of_ `any`
        - `SWITCH` — array
          - _array of_ `any`
        - `3SWITCH` — array
          - _array of_ `any`
        - `GPICKUP` — object
          - `1` — string
          - `2` — string
          - `3` — string
        - `QPICKUP` — object
          - `1` — string
          - `2` — string
          - `3` — string
          - `4` — string
          - `5` — string
        - `QCALL` — object
          - `1` — string
          - `2` — string
          - `3` — string
          - `4` — string
          - `5` — string
    - `features` — object
      - `internal` — featureType
        - `away` — object
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `dnd` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `default` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
      - `external` — featureType
        - `away` — object
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `dnd` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `default` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
      - `blacklist` — featureType
        - `away` — object
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `dnd` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `default` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
      - `whitelist` — featureType
        - `away` — object
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `dnd` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
        - `default` — featureStatusStructure
          - `_ACTIVATED` — object
            - `status` — string
          - `MEXT` — object
            - `status` — string
            - `value` — string
          - `BCF` — object
            - `status` — string
            - `value` — string
          - `UCF` — object
            - `status` — string
            - `value` — string
          - `SMSMCN` — object
            - `status` — string
          - `REJECT` — object
            - `status` — string
          - `EMAILMCN` — object
            - `status` — string
          - `FCF` — object
            - `status` — string
            - `value` — string
          - `TOUT` — object
            - `status` — string
            - `value` — string
          - `CW` — object
            - `status` — string
          - `MOBCONFIRMATION` — object
            - `status` — string
          - `RING` — object
            - `status` — string
            - `value` — string
    - `sharedvm` — object
      - `status` — string
      - `value` — string
    - `cwtone` — object
      - `status` — string
    - `contactCenter` — object
      - `enable` — bool **(required)**
      - `statusSync` — bool **(required)**
      - `callGroups` — array **(required)**
        - _array of_ `object`
          - `id` — integer **(required)**
          - `isStatic` — bool
          - `active` — bool **(required)**
          - `title` — string
          - `cid` — string
    - `popupUrl` — object
      - `url` — string
      - `outgoing` — string _(enum: `click`, `ring`, `up`)_
      - `incoming` — string _(enum: `click`, `ring`, `up`)_
- Errors: `401`, `500`

#### `PUT` `/Personal/settings/`

Update settings

- operationId: `updateSettings`
- **Request body** (`application/json`)
  - `undefined` — object
- **Response 200**
  - `type` — string
  - `result` — string
- Errors: `400`, `401`, `500`

#### `GET` `/Personal/PagingGroups/`

Get paging groups

- operationId: `getPagingGroups`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `total` — int
    - `records` — array
      - _array of_ `object`
        - `id` — string
        - `name` — string
- Errors: `401`, `500`

#### `GET` `/Personal/Token/`

**Generate token**

PBX token authentication includes two steps: token generation via API and its usage in any request to PBX by adding GET parameter ?token=RETRIVED_TOKEN_HERE. In case of successful token authentication, you are redirected to the same page, but without token parameter. Generated token can be used only for one authentication.

- operationId: `getToken`
- **Parameters**
  - `type` (query) — string — JWT
  - `service` (query) — string — generates a token for authentication to auth.wildix.com
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `token` — string
- Errors: `401`, `500`

#### `PUT` `/Personal/Presence/`

Update personal presence

- operationId: `updatePresence`
- **Request body** (`application/json`) **(required)**
  - `status` — string **(required)** — Possible values: available, away, dnd, mur
  - `message` — string _(default=empty)_
  - `until` — string — Format: "19/09/2017 11:30" in UTC _(default=empty)_
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

#### `PUT` `/Personal/Presence/location/`

Update personal location

- operationId: `updatePresenceLocation`
- **Request body** (`application/json`)
  - `lat` — string — latitude
  - `lng` — string — longitude
  - `address` — string — text address
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

#### `PUT` `/personal/roster/`

Update a personal roster

- operationId: `updatePresenceRoster`
- **Request body** (`application/json`)
  - `users` — array
    - _array of_ `any`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `500`

#### `POST` `/personal/login/`

User authentication

- operationId: `login`
- **Request body** (`application/json`) **(required)**
  - `login` — string **(required)** — The username or extension
  - `password` — string **(required)** — The user password
  - `remember` — string **(required)** — Remember session for a week, value 0 or 1
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=OK)_
- Errors: `400`, `500`

#### `GET` `/personal/logout/`

User logout

- operationId: `logout`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=OK)_
- Errors: `401`, `500`

#### `GET` `/api/v2/personal/features/`

**Get personal features**

Get user personal features including status, popup URL, web app, two-factor authentication, date/time settings, and predefined statuses.

- operationId: `getPersonalFeatures`
- **Parameters**
  - `uid` (query) — string — User ID. If not provided, returns features for the authenticated user. **Root users have full access. Administrators require VIEW permission for cross-user access. Regular users can only access their own features.**
  - `fields` (query) — string — Comma-separated list of feature types to return. Available values: personal, callClasses, telephony, functionKeys, contactCenter, roster, ringtones.
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `personal` — object
      - `ctiOptions` — object — CTI options for collaboration and fax features
        - `fax_options_from_company` — string — Company name for fax header
        - `fax_options_stationid` — string — Fax station ID
        - `fax_options_headerinfo` — string — Fax header information
        - `unread_messages_via_email` — boolean — Send unread messages via email
      - `dateTime` — object
        - `is24h` — boolean — Use 24-hour time format
        - `format` — string — Date format
      - `predefinedStatus` — object — Predefined status messages (max 100 entries)
        - _map of_ `object`
          - `status` — string — Status type _(enum: `available`, `away`, `dnd`)_
          - `message` — string — Status message (max 1000 characters) _(maxLen=1000)_
          - `duration` — integer — Duration in seconds (0 for indefinite, max 86400 = 24 hours) _(min=0; max=86400)_
      - `popupUrl` — object
        - `url` — string — CRM popup URL template
        - `outgoing` — string — When to show popup for outgoing calls _(enum: `click`, `up`, `ring`)_
        - `incoming` — string — When to show popup for incoming calls _(enum: `click`, `up`, `ring`)_
      - `twoFactor` — object
        - `type` — string — Two-factor authentication type _(enum: `totp`, `email`, `sms`)_
        - `enable` — boolean — Two-factor authentication enabled
        - `app` — string — Authenticator app name
        - `sync_timestamp` — boolean — Sync timestamp
      - `webApp` — object
        - `enable` — boolean — Web app integration enabled
        - `url` — string — Web app URL
    - `callClasses` — object — Call class features with blacklist, whitelist, external, and internal configurations
      - `blacklist` — object — Blacklist call class settings for different statuses
      - `whitelist` — object — Whitelist call class settings for different statuses
      - `external` — object — External call class settings for different statuses
      - `internal` — object — Internal call class settings for different statuses
    - `telephony` — object — Telephony features and settings
      - `currentServiceId` — string — Current service ID
      - `customIdentities` — string — Custom identities (comma-separated)
      - `sharedVoiceMail` — object
        - `status` — boolean
        - `value` — string
      - `callWaitingTone` — boolean — Call waiting tone enabled
      - `hotline` — object
        - `status` — boolean
        - `value` — string
        - `delay` — string
      - `road` — boolean — Road warrior mode
      - `telephoneBlocked` — boolean — Telephone blocked status
    - `functionKeys` — object — Function key configurations
      - _map of_ `object`
        - `key` — string — Function key type
        - `value` — string — Function key value
        - `title` — string — Function key title
        - `directTransfer` — boolean — Direct transfer enabled
        - `audioNotification` — boolean — Audio notification enabled
        - `viewCalls` — boolean — View calls enabled
    - `contactCenter` — object — Contact center features and call group settings
      - `enable` — boolean — Contact center enabled
      - `statusSync` — boolean — Status synchronization enabled
      - `callGroups` — object — Call groups configuration
      - `whitelistEnable` — boolean — Whitelist enabled
      - `whitelistCallGroups` — object — Whitelist call groups
      - `alternatePickupCallGroups` — string — Alternate pickup call groups
      - `alternatePickupGroups` — string — Alternate pickup groups
    - `roster` — object — Roster configuration with contact groups
      - _map of_ `array`
        - _array of_ `object`
          - `displayName` — string
          - `extension` — string
    - `ringtones` — object — Available ringtones with file formats
      - _map of_ `array`
        - _array of_ `string`
- Errors: `400`, `401`, `403`, `500`

#### `POST` `/api/v2/personal/features/`

**Update personal features**

Update user personal features including status, popup URL, web app, two-factor authentication, date/time settings, and predefined statuses.

- operationId: `updatePersonalFeatures`
- **Parameters**
  - `uid` (query) — string — User ID or comma-separated list of user IDs. If not provided, updates features for the authenticated user. **Root users have full access. Administrators require VIEW permission for cross-user modification and specific feature ACL permissions. Regular users require feature-specific ACL permissions for self-modification.** For bulk updates, roster features are ignored.
- **Request body** (`application/json`) **(required)**
  - `ctiOptions` — object — CTI options for collaboration and fax features
    - `fax_options_from_company` — string — Company name for fax header
    - `fax_options_stationid` — string — Fax station ID
    - `fax_options_headerinfo` — string — Fax header information
    - `unread_messages_via_email` — boolean — Send unread messages via email
  - `dateTime` — object
    - `is24h` — boolean — Use 24-hour time format
    - `format` — string — Date format
  - `predefinedStatus` — object — Predefined status messages (max 100 entries). You can send either indexed entries ("1", "2", etc.) or a single status object for auto-indexing.
    - _map of_ `object`
      - `status` — string — Status type _(enum: `available`, `away`, `dnd`)_
      - `message` — string — Status message (max 1000 characters) _(maxLen=1000)_
      - `duration` — integer — Duration in seconds (0 for indefinite, max 86400 = 24 hours) _(min=0; max=86400)_
  - `popupUrl` — object
    - `url` — string — CRM popup URL template
    - `outgoing` — string — When to show popup for outgoing calls _(enum: `click`, `up`, `ring`)_
    - `incoming` — string — When to show popup for incoming calls _(enum: `click`, `up`, `ring`)_
  - `twoFactor` — object
    - `type` — string — Two-factor authentication type _(enum: `totp`, `email`, `sms`)_
    - `enable` — boolean — Two-factor authentication enabled
    - `app` — string — Authenticator app name
  - `webApp` — object
    - `enable` — boolean — Web app integration enabled
    - `url` — string — Web app URL
  - `currentServiceId` — string — Current telephony service ID
  - `customIdentities` — string — Custom identities (comma-separated)
  - `sharedVoiceMail` — object
    - `status` — boolean
    - `value` — string
  - `callWaitingTone` — boolean — Call waiting tone enabled
  - `hotline` — object
    - `status` — boolean
    - `value` — string
    - `delay` — string
  - `road` — boolean — Road warrior mode
  - `telephoneBlocked` — boolean — Telephone blocked status
  - `functionKeys` — object — Function key configurations. You can send either indexed entries ("1", "2", etc.) or a single function key object for auto-indexing.
    - _map of_ `object`
      - `key` — string — Function key type
      - `value` — string — Function key value
      - `title` — string — Function key title
      - `directTransfer` — boolean — Direct transfer enabled
      - `audioNotification` — boolean — Audio notification enabled
      - `viewCalls` — boolean — View calls enabled
  - `personal` — object — Nested format
    - `ctiOptions` — object — CTI options
    - `dateTime` — object — Date/time settings
    - `predefinedStatus` — object — Predefined status messages
    - `popupUrl` — object — Popup URL settings
    - `twoFactor` — object — Two-factor authentication
    - `webApp` — object — Web app integration
  - `callClasses` — object — Call class features to update with blacklist, whitelist, external, and internal configurations
  - `telephony` — object — Telephony features to update including service settings and call handling
  - `contactCenter` — object — Contact center features to update including call groups and settings
  - `roster` — object — Roster features to update (ignored in bulk operations)
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — union
    - _oneOf_ — exactly one of:
      - **`success`**
        - `success` — boolean — Update result for single user
      - **`object`**
        - _map of_ `object`
          - `success` — boolean
          - `error` — string — Error message if update failed
- Errors: `400`, `401`, `403`, `500`

#### `GET` `/personal/locations/`

**Get list of locations**

- operationId: `trustedIpsGet`
- **Parameters**
  - `ip` (query) — string — IP address
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `companyId` — string
        - `userId` — int
        - `ip` — string
        - `country` — string
        - `fullAddress` — string
        - `updatedAt` — string
- Errors: `401`, `500`

#### `DELETE` `/personal/locations/{ip}`

**Remove location**

- operationId: `trustedIpsDelete`
- **Parameters**
  - `ip` (path) — string **(required)** — IP address
- **Response 200** (`ApiResponseTrue`)
  - `type` — string _(enum: `result`)_
  - `result` — boolean _(enum: `True`)_
- Errors: `401`, `404`, `500`

### Trunk groups

#### `GET` `/Trunks/Groups/`

**Get trunk groups**

Returns the list of trunk groups with rules

- operationId: `GetTrunkGroups`
- **Scopes**: `trunks:read`, `pbx:read`
- **Company API Key scope**: `trunks:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Trunk group id.
        - `name` — string — Trunk group name.
        - `description` — string — Trunk group description.
        - `rules` — array
          - _array of_ `object`
            - `priority` — integer — Trunk group rule priority.
            - `trunkName` — string — Trunk group rule name.
            - `prepend` — string — Trunk group rule prepend.
            - `remove` — string — Delete trunk group rule.
            - `maxCalls` — integer — Trunk group rule concurent max calls count.
            - `timeout` — integer — Trunk group rule timeout.
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/Trunks/Groups/`

**Create trunk group**

Create trunk group with rules

- operationId: `CreateTrunkGroup`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

#### `PUT` `/Trunks/Groups/{id}`

**Edit trunk group**

Edit trunk group with rules

- operationId: `EditTrunkGroup`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`

#### `DELETE` `/Trunks/Groups/{id}`

**Delete trunk group**

Delete trunk group with rules

- operationId: `deleteTrunkGroup`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`, `404`

### Trunks

#### `GET` `/Trunks/Sip/`

**Get SIP trunks**

Get the list of SIP trunks

- operationId: `GetTrunksSIP`
- **Scopes**: `trunks:read`, `pbx:read`
- **Company API Key scope**: `trunks:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — ID SIP
        - `title` — string — Trunk title
        - `name` — string — Auth Login. Provided by the VoIP Carrier for authentication
        - `register` — string — SIP Register string
        - `settingsPbx` — object — Trunk PBX settings
          - `audioCodecs` — array — List of audio codecs supported by the trunk
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `allowTransfer` — boolean — Support Refer and Hold. Allow the trunk to perform transfers and disable hold requests from the trunk
          - `cidBody` — string — Indicate the contents of the cid header
          - `cidHeader` — string — Additional header to set the cid number
          - `contactNumber` — string — Contact number
          - `context` — string — Dialplan procedure for routing calls coming from this trunk
          - `countryCode` — integer — Used for number normalization, specify the code of the country where the trunk is used. Integer or null.
          - `isoCode` — string — ISO 3166 country code
          - `diversionHeader` — string — SIP header Diversion for outgoing INVITE to trunk in order to preserve the information on the original called number in case of call forwarding
          - `historyInfoHeader` — string — SIP header History-info for outgoing INVITE to trunk in order to preserve the information on the original called number in case of call forwarding
          - `forceSrtp` — boolean — Enable/Disable SDES-SRTP protocol for calls through the trunk
          - `fromDomain` — string — Forced from domain header and used in register and invite SIP messages
          - `fromUser` — string — Forced from number header and used for invite messages and for registration
          - `fromNumber` — string — Expression to set a dynamic cid number for outgoing calls based on the office number or on the value; works only if the operator allows setting of a cid number for outgoing calls
          - `fromName` — string — Regular expression to set a dynamic cid name for outgoing calls
          - `host` — string — Address or host name of sip proxy; dynamic indicates that the trunk is used for incoming registration (incoming invites are allowed)
          - `peername` — string — Trunk name
          - `port` — string — Port for address or host name of sip proxy
          - `preserveOrigCid` — boolean — Show original caller number. can be used by operators which support displaying any number as cid, allows displaying original caller number from trunk in case of transfers/ mobility calls
          - `priceList` — integer — Associated pricelist for the correct calculation of calls cost
          - `privacyHeader` — string — Privacy Header
          - `qualify` — bolean — Keep-Alive. Enable/disable periodic sending of keep alive messages to the trunk
          - `dtmfMode` — string — Allows you to select the DTMF transfer mode
          - `rfcPayload` — integer — Specify the payload for DTMF transfer mode
          - `rport` — string — The rport mechanism changes the SIP routing behavior, so that responses can be received through a NAT even if private addresses are used in the SIP headers
          - `secret` — string — Password for authentication provided by the VoIP Carrier
          - `sessionExpires` — integer — Maximum seconds of the session timer
          - `sessionMinse` — integer — Minimum seconds of the session timer
          - `sessionTimer` — boolean — Enable/disable the check of the session validity to avoid pending calls
          - `ssrcChange` — boolean — Force static SSRC. Forbid SSRC change in RTP sessions; this option is recommended for some SIP operators which do not playback RTP packets after change of SSRC
          - `thirtyEightPtUdptl` — booelan — Enable/disable special parameters for T38 support
          - `thirtyEightPtErrorCorrection` — string — T38 error correction
          - `thirtyEightPtMaxDatagram` — integer — T38 maxdatagram
          - `toneZone` — string — The country for the correct tone recognition
          - `transportWildix` — string — Transport protocol to be used
          - `trustRpid` — boolean — Incoming CID. Setting of a specific SIP header from which Cid header must be retrieved
          - `userName` — string — Auth Login. Provided by the VoIP Carrier for authentication
          - `videoCodecs` — boolean — Enable/disable the video codecs supported by the trunk
          - `playRemoteMoh` — boolean — Play remote MoH. configure remote music on hold to be played instead of the local one for external calls
          - `type` — string — Trunk type
          - `symmetricRtp` — boolean — Enable/disable symmetric Rtp
          - `language` — string — Language
          - `insecure` — string — Insecure
          - `disallow` — string — Dissalow
          - `kernelLevelMedia` — boolean — Enable Kernel-level Media Forwarding
        - `settingsWms` — object — Trunk WMS settings
          - `dnsServer` — string — Custom DNS Server. Used to resolve the sip proxy domain name
          - `enableReg` — boolean — Enable registration. Enable/disable outgoing registration (in case of PBXs SIP interconnection, it is enabled on the Client PBX SIP trunk and disabled on Server)
          - `expiry` — integer — Registration Expiry (sec). Set the expiry time for outgoing register messages.
          - `natIp` — string — NAT IP. Enable/disable the network connection IP
          - `outboundProxy` — string — All outgoing SIP messages are sent through the indicated host
          - `outboundProxyPort` — string — Outbound proxy port
          - `overwriteReg` — boolean — Enable/disable registration proxy
          - `regHost` — string — IP address or host name of a proxy server
          - `regPort` — string — Port of a proxy server
          - `regFromUser` — string — Forced from number header and used for invite messages and for registration proxy
          - `regSecret` — string — Password. Credentials for access of a proxy server
          - `regUsername` — string — Login. Credentials for access of a proxy server
        - `status` — object — Trunk active status
          - `outgoing` — object
            - `state` — string — State of outgoing SIP registration
            - `title` — string — Title of outgoing SIP registration
          - `incoming` — object
            - `state` — string — State of incoming SIP registration
            - `title` — string — Title of incoming SIP registration
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `POST` `/Trunks/Sip/`

**Create SIP trunk**

Create SIP trunks

- operationId: `CreateTrunksSIP`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Request body** (`application/json`)
  - `title` — string **(required)** — Trunk title
  - `name` — string **(required)** — Trunk name
  - `register` — string — SIP Register string
  - `settingsPbx` — object **(required)** — Trunk PBX settings
    - `audioCodecs` — array — List of audio codecs supported by the trunk
      - _array of_ `object`
        - `key` — string — Name of codec
        - `value` — string — Value of codec
        - `enable` — boolean — Enable/disable support codec
    - `allowTransfer` — boolean — Support Refer and Hold. Allow the trunk to perform transfers and disable hold requests from the trunk
    - `cidBody` — string — Indicate the contents of the cid header
    - `cidHeader` — string — Additional header to set the cid number
    - `contactNumber` — string — Contact number
    - `context` — string — Dialplan procedure for routing calls coming from this trunk
    - `countryCode` — integer — Used for number normalization, specify the code of the country where the trunk is used. Integer or null.
    - `isoCode` — string — ISO 3166 country code
    - `diversionHeader` — string — SIP header Diversion for outgoing INVITE to trunk in order to preserve the information on the original called number in case of call forwarding
    - `historyInfoHeader` — string — SIP header History-info for outgoing INVITE to trunk in order to preserve the information on the original called number in case of call forwarding
    - `forceSrtp` — boolean — Enable/Disable SDES-SRTP protocol for calls through the trunk
    - `fromDomain` — string — Forced from domain header and used in register and invite SIP messages
    - `fromUser` — string — Forced from number header and used for invite messages and for registration
    - `fromNumber` — string — Expression to set a dynamic cid number for outgoing calls based on the office number or on the value; works only if the operator allows setting of a cid number for outgoing calls
    - `fromName` — string — Regular expression to set a dynamic cid name for outgoing calls
    - `host` — string — Address or host name of sip proxy; dynamic indicates that the trunk is used for incoming registration (incoming invites are allowed)
    - `peername` — string — Trunk name
    - `port` — string — Port for address or host name of sip proxy
    - `preserveOrigCid` — boolean — Show original caller number. can be used by operators which support displaying any number as cid, allows displaying original caller number from trunk in case of transfers/ mobility calls
    - `priceList` — integer — Associated pricelist for the correct calculation of calls cost
    - `privacyHeader` — string — Privacy Header
    - `qualify` — bolean — Keep-Alive. Enable/disable periodic sending of keep alive messages to the trunk
    - `dtmfMode` — string — Allows you to select the DTMF transfer mode
    - `rfcPayload` — integer — Specify the payload for DTMF transfer mode
    - `rport` — string — The rport mechanism changes the SIP routing behavior, so that responses can be received through a NAT even if private addresses are used in the SIP headers
    - `secret` — string — Password for authentication provided by the VoIP Carrier
    - `sessionExpires` — integer — Maximum seconds of the session timer
    - `sessionMinse` — integer — Minimum seconds of the session timer
    - `sessionTimer` — boolean — Enable/disable the check of the session validity to avoid pending calls
    - `ssrcChange` — boolean — Force static SSRC. Forbid SSRC change in RTP sessions; this option is recommended for some SIP operators which do not playback RTP packets after change of SSRC
    - `thirtyEightPtUdptl` — booelan — Enable/disable special parameters for T38 support
    - `thirtyEightPtErrorCorrection` — string — T38 error correction
    - `thirtyEightPtMaxDatagram` — integer — T38 maxdatagram
    - `toneZone` — string — The country for the correct tone recognition
    - `transportWildix` — string — Transport protocol to be used
    - `trustRpid` — boolean — Incoming CID. Setting of a specific SIP header from which Cid header must be retrieved
    - `userName` — string — Auth Login. Provided by the VoIP Carrier for authentication
    - `videoCodecs` — boolean — Enable/disable the video codecs supported by the trunk
    - `playRemoteMoh` — boolean — Play remote MoH. configure remote music on hold to be played instead of the local one for external calls
    - `type` — string — Trunk type
    - `symmetricRtp` — boolean — Enable/disable symmetric Rtp
    - `language` — string — Language
    - `insecure` — string — Insecure
    - `disallow` — string — Dissalow
    - `kernelLevelMedia` — boolean — Enable Kernel-level Media Forwarding
  - `settingsWms` — object **(required)** — Trunk WMS settings
    - `dnsServer` — string — Custom DNS Server. Used to resolve the sip proxy domain name
    - `enableReg` — boolean — Enable registration. Enable/disable outgoing registration (in case of PBXs SIP interconnection, it is enabled on the Client PBX SIP trunk and disabled on Server)
    - `expiry` — integer — Registration Expiry (sec). Set the expiry time for outgoing register messages.
    - `natIp` — string — NAT IP. Enable/disable the network connection IP
    - `outboundProxy` — string — All outgoing SIP messages are sent through the indicated host
    - `outboundProxyPort` — string — Outbound proxy port
    - `overwriteReg` — boolean — Enable/disable registration proxy
    - `regHost` — string — IP address or host name of a proxy server
    - `regPort` — string — Port of a proxy server
    - `regFromUser` — string — Forced from number header and used for invite messages and for registration proxy
    - `regSecret` — string — Password. Credentials for access of a proxy server
    - `regUsername` — string — Login. Credentials for access of a proxy server
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `403`

#### `PUT` `/Trunks/Sip/{id}`

**Update SIP trunk**

Update SIP trunk by ID

- operationId: `UpdateTrunksSip`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Trunk ID
- **Request body** (`application/json`)
  - `title` — string **(required)** — Trunk title
  - `name` — string **(required)** — Trunk name
  - `settingsPbx` — object **(required)** — Trunk PBX settings
    - `audioCodecs` — array
      - _array of_ `object`
        - `enable` — boolean — Codec enabled
        - `key` — string — Codec name
        - `value` — string — Ptime in ms
    - `allowTransfer` — boolean — Support Refer and Hold
    - `cidBody` — string — Cid Body
    - `cidHeader` — string — Cid Header
    - `contactNumber` — string — Contact number
    - `context` — string — Dialplan
    - `countryCode` — integer — Country Code
    - `isoCode` — string — ISO 3166 country code
    - `disallow` — string — Disallow
    - `diversionHeader` — string — Diversion Header
    - `dtmfMode` — string — DTMF mode
    - `forceSrtp` — boolean — SDES-SRTP
    - `fromDomain` — string — From domain
    - `fromName` — string — From name
    - `fromNumber` — string — From number
    - `fromUser` — string — From user
    - `historyInfoHeader` — string — History-Info Header
    - `host` — string — Host Name
    - `insecure` — string — Insecure
    - `language` — string — Language
    - `peername` — string — Trunk name
    - `port` — string — Port
    - `preserveOrigCid` — boolean — Show original caller number
    - `priceList` — integer — Price list
    - `privacyHeader` — string — Privacy Header
    - `qualify` — string — Qualify
    - `rfcPayload` — integer — Payload 2833 rfc
    - `rport` — string — Rport
    - `secret` — string — Password
    - `sessionExpires` — integer — Session Timer max
    - `sessionMinse` — integer — Session Timer min
    - `sessionTimer` — boolean — Session Timer enabled
    - `ssrcChange` — boolean — Force static SSRC
    - `symmetricRtp` — boolean — Symmetric Rtp
    - `thirtyEightPtUdptl` — booelan — T38 enabled
    - `thirtyEightPtErrorCorrection` — string — T38 error correction
    - `thirtyEightPtMaxDatagram` — integer — T38 Maxdatagram
    - `toneZone` — string — Tone Zone
    - `transportWildix` — string — Transport
    - `trustRpid` — boolean — Incoming CID
    - `type` — string — Registration Proxy enabled
    - `userName` — string — Auth Login
    - `videoCodecs` — boolean — Allow video codecs
    - `kernelLevelMedia` — boolean — Enable Kernel-level Media Forwarding
  - `settingsWms` — object **(required)** — Trunk WMS settings
    - `dnsServer` — string — Custom DNS Server
    - `enableReg` — boolean — Enable registration
    - `expiry` — integer — Registration Expiry (sec)
    - `natIp` — string — NAT IP
    - `outboundProxy` — string — Outbound proxy
    - `outboundProxyPort` — string — Outbound proxy port
    - `overwriteReg` — boolean — Overwrite registration
    - `regFromUser` — string — From user
    - `regHost` — string — Reg Host
    - `regPort` — string — Host Port
    - `regSecret` — string — Password
    - `regUsername` — string — Username
  - `status` — object
    - `outgoing` — object
      - `state` — string — Sip registration outgoing status
      - `title` — string — Sip registration outgoing status title
    - `incoming` — object
      - `state` — string — Sip registration incoming status
      - `title` — string — Sip registration incoming status title
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `401`, `403`, `404`

#### `DELETE` `/Trunks/Sip/{id}`

**Delete SIP trunk**

Delete SIP trunk by ID

- operationId: `deleteSipTrunk`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/Trunks/Pstn/`

**Get PSTN trunks**

Returns the list of PSTN trunks

- operationId: `GetTrunksPSTN`
- **Scopes**: `trunks:read`, `pbx:read`
- **Company API Key scope**: `trunks:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Trunk ID.
        - `name` — string — Trunk name
        - `title` — string — Trunk title
        - `ports` — integer — Number of trunk ports
        - `technology` — string — Trunk technology
        - `address` — string — IP device address
        - `settingsPbx` — object — Trunk PBX settings
          - `username` — string — Trunk name
          - `type` — string — Trunk type
          - `secret` — string — Password
          - `insecure` — string — Insecure
          - `fromUser` — string — From user
          - `dtmfmode` — string — DTMF mode
          - `context` — string — Context
          - `host` — string — Host
          - `port` — integer — Port
        - `settingsMgw` — object — Trunk MGW settings
          - `currentDetected` — string — Open switching interval
          - `polarityNormalDetected` — string — Polarity reversal
          - `busyToneDetected` — string — Busy tone
          - `currentDisconnectThreshold` — string — Current disconnect threshold
          - `fskCidField` — string — FSK CID field
          - `toneZone` — string — Country or region
          - `dcImpedance` — string — DC Impedance
          - `impedance` — string — Impedance
          - `lineType` — string — Line type
          - `silenceDetection` — string — Silence detection
          - `silenceDetectionEnabled` — string — Silence detection enable
          - `voipOutputGain` — integer — Gain TX VoIP
          - `voipInputGain` — integer — Gain RX VoIP
          - `bearerCapG711` — integer — Used by the calling party to specify the kind of B channel that is being requested. It is indicated in the Q.931 SETUP message and it is used to distinguish among the different types of voice and data calls
          - `bearerCapG729` — integer — Used by the calling party to specify the kind of B channel that is being requested. It is indicated in the Q.931 SETUP message and it is used to distinguish among the different types of voice and data calls
          - `priceList` — integer — Pricelists
          - `dtmfDebounce` — string — DTMF debounce
          - `smsDeliveryTries` — integer — SMS delivery attempts
          - `busyResponse` — integer — Response on port busy
          - `language` — string — Language
          - `countryCode` — integer — Used for number normalization
          - `isoCode` — string — ISO 3166 country code
          - `dialTone` — string — Default Tone. Country for the correct tone recognition
          - `preserveOrigCid` — boolean — Show original caller number. Can be used by operators which support displaying any number as cid, allows displaying original caller number from trunk in case of transfers/mobility calls
          - `poundSupport` — boolean — Escape Pound (#) In SIP URI Username. Enables support of pound (#) symbol in called number, normally used as a confirmation to send number; as a rule it is used in integrations with legacy PBXs
          - `clockReferencePort` — integer — Port selection for clock management
          - `ports` — array — Device ports
            - _array of_ `object`
              - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `status` — object — Trunk active status
          - `active` — boolean — State of trunk status
          - `title` — string — Title of trunk status
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `PUT` `/Trunks/Pstn/{id}/`

**Update PSTN trunk**

Update PSTN trunk by ID

- operationId: `PutTrunksPSTN`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Trunk ID
- **Request body** (`application/json`)
  - `name` — string **(required)** — Trunk name
  - `title` — string — Trunk title
  - `ports` — integer — Number of trunk ports
  - `technology` — string **(required)** — Trunk technology
  - `address` — string — IP device address
  - `settingsPbx` — object **(required)** — Trunk PBX settings
    - `username` — string **(required)** — Trunk name
    - `type` — string — Trunk type
    - `secret` — string — Password
    - `insecure` — string — Insecure
    - `fromUser` — string — From user
    - `dtmfmode` — string — DTMF mode
    - `context` — string — Context
    - `host` — string — Host
    - `port` — integer — Port
  - `settingsMgw` — object **(required)** — Trunk MGW settings
    - `currentDetected` — string — Open switching interval
    - `polarityNormalDetected` — string — Polarity reversal
    - `busyToneDetected` — string — Busy tone
    - `currentDisconnectThreshold` — string — Current disconnect threshold
    - `fskCidField` — string — FSK CID field
    - `toneZone` — string — Country or region
    - `dcImpedance` — string — DC Impedance
    - `impedance` — string — Impedance
    - `lineType` — string — Line type
    - `silenceDetection` — string — Silence detection
    - `silenceDetectionEnabled` — string — Silence detection enable
    - `voipOutputGain` — integer — Gain TX VoIP
    - `voipInputGain` — integer — Gain RX VoIP
    - `bearerCapG711` — integer — Used by the calling party to specify the kind of B channel that is being requested. It is indicated in the Q.931 SETUP message and it is used to distinguish among the different types of voice and data calls
    - `bearerCapG729` — integer — Used by the calling party to specify the kind of B channel that is being requested. It is indicated in the Q.931 SETUP message and it is used to distinguish among the different types of voice and data calls
    - `priceList` — integer — Pricelists
    - `dtmfDebounce` — string — DTMF debounce
    - `smsDeliveryTries` — integer — SMS delivery attempts
    - `busyResponse` — integer — Response on port busy
    - `language` — string — Language
    - `countryCode` — integer — Used for number normalization
    - `isoCode` — string — ISO 3166 country code
    - `dialTone` — string — Default Tone. Country for the correct tone recognition
    - `preserveOrigCid` — boolean — Show original caller number. Can be used by operators which support displaying any number as cid, allows displaying original caller number from trunk in case of transfers/mobility calls
    - `poundSupport` — boolean — Escape Pound (#) In SIP URI Username. Enables support of pound (#) symbol in called number, normally used as a confirmation to send number; as a rule it is used in integrations with legacy PBXs
    - `clockReferencePort` — integer — Port selection for clock management
    - `ports` — array — Device ports
      - _array of_ `object`
        - `port` — integer — Number of port
        - `callingNameMaxLength` — integer — Specify the max length of the calling name
        - `cedToneDetection` — boolean — Allow voice and fax calls on the same line; enable the gateway to detect
        - `cngToneDetection` — boolean — Allow voice and fax calls on the same line; enable the gateway to detect
        - `channelAllocationStrategy` — integer — Channel allocation strategy for this port
        - `clock` — integer — Select between Generate clock(200) and Use provided clock(300) modes
        - `connectionType` — integer — Type of ISDN connection between Point-to-Point(100) and Point-to-Multipoint(200)
        - `context` — string — Dialplan procedure for routing calls coming from this trunk
        - `correctIncomingCallingNumbers` — boolean — Used for correct caller number visualization (adds 0 to national and 00 to international calls)
        - `destinationCode` — string — Specify the area code
        - `detectionThreshold` — integer — Set up the threshold level for FAX detection
        - `endpointType` — integer — select between Terminal Equipment(100) (connection to public ISDN) or Network Termination(200) modes (connection to ISDN phones or other devices in TE mode, e.g. PBXs)
        - `facilityServices` — boolean — Cid Name via Facility IE. Enable/disable the gateway to accept Facility messages and enables calling name delivery for US and Canada
        - `inbandDtmfDialing` — boolean — Enable/disable recognition of inband DTMF tones
        - `lineCoding` — integer — Line coding schemes. Bipolar 8-Zero Substitution (100), High Density Bipolar 3 (200), Alternate Mark Inversion (300)
        - `linkEstablishment` — integer — Select the connection establishment type between Permanent(200) and On Demand(100)
        - `maximumFacilityWaitingDelay` — integer — Maximum waiting time of a Facility request
        - `networkType` — integer — Type of the ISDN network
        - `overlap` — boolean — Enable/disable the gateway to begin processing a call as soon as it can determine a destination from dialed digits that form only part of a complete number
        - `priceList` — integer — The pricelist to calculate the costs for calls through the trunk
        - `progressIndicatorInAlerting` — boolean — Indicator in alerting. Enable/disable the gateway to provide the tone of progress during the indicated operation
        - `progressIndicatorInCallProgressForSetup` — boolean — Indicator in call progress for setup. Enable/disable the gateway to provide the tone of progress during the indicated operation
        - `progressIndicatorInConnect` — boolean — Indicator in connect. Enable/disable the gateway to provide the tone of progress during the indicated operation
        - `progressIndicatorInProgress` — boolean — Indicator in progress. Enable/disable the gateway to provide the tone of progress during the indicated operation
        - `progressIndicatorInSetup` — boolean — Indicator in setup. Enable/disable the gateway to provide the tone of progress during the indicated operation
        - `progressIndicatorInSetupAck` — boolean — Indicator in setup ack. Enable/disable the gateway to provide the tone of progress during the indicated operation
        - `sendRestartOnStartup` — boolean — Enable/disable sending of restart request to the operator each time the gateway reboots
        - `sendingComplete` — boolean — Enable/disable include Sending Complete information element into setup message
        - `signalInformationElement` — boolean — Enable/disable the use of Signal Information Element field to provide tones during different stages of call processing
        - `signalProtocol` — integer — Asymmetric and symmetric signaling protocol. DSS1 - 100, DMS100 - 200, NI2 - 300, 5ESS - 400, QSIG - 500
        - `useImplicitInbandInfo` — boolean — Enable/disable the use of tones coming from endpoints
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`, `404`

#### `GET` `/Trunks/Fxo/`

**Get FXO trunks**

Get the list of FXO trunks

- operationId: `GetTrunksFXO`
- **Scopes**: `trunks:read`, `pbx:read`
- **Company API Key scope**: `trunks:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Trunk ID.
        - `username` — string — Trunk name
        - `title` — string — Trunk title.
        - `technology` — string — Trunk technology.
        - `address` — string — IP device address
        - `model` — string — Model device
        - `status` — object — Device status
          - `active` — boolean — On/Off
          - `title` — string — Registration host
        - `settingsMgw` — object — Trunk MGW settings.
          - `toneZone` — string — Country or region
          - `countryCode` — integer — Used for number normalization
          - `isoCode` — string — ISO 3166 country code
          - `impedance` — integer — Impedance values to avoid noise during line connection
          - `dcImpedance` — boolean — DC Impedance (disabled by default)
          - `fskCidField` — string — Obtain FSK CID (available for W04FXO 2020), value to display the correct Caller ID
          - `busyToneDetected` — boolean — Disconnect signaling - busy tone (available for W04FXO R3)
          - `polarityNormalDetected` — boolean — Disconnect signaling - polarity reversal (available for W04FXO R3). This parameter to avoid dropped calls due to a wrong detection of polarity change on the copper line
          - `currentDetected` — boolean — Disconnect signaling - open switching interval (available for W04FXO R3)
          - `currentDisconnectThreshold` — integer — Current Disconnect Threshold in ms
          - `silenceDetectionEnabled` — boolean — Silence detection (available for W04FXO R3). Enable/ disable this parameter as the cause for disconnecting the call
          - `silenceDetection` — integer — Silence detection timeout in second (available for W04FXO R3)
          - `ports` — object — Device ports
            - `port` — integer — Number of port
            - `priceList` — integer — The pricelist to calculate the costs for calls through the trunk
            - `destinationCode` — string — Specify the area code
            - `context` — string — Dialplan procedure for routing calls coming from this trunk
            - `hotlineNumber` — string — The number corresponding to the line which is present in the associated Dialplan procedure
            - `pstnRingCount` — boolean — Detect caller ID (available for W04FXO 2020). Enable/disable caller ID detection
            - `cidType` — integer — Caller ID type (available for W04FXO 2020). The standard for transmitting the caller ID information
            - `flashTime` — integer — Flash time (available for FXO gateways pre 2020). Timeout (in msec) for hookflash detection
            - `answerTime` — integer — Dialing answer delay time. Interdigit dial timeout (in sec), when terminated, the call is sent to trunk
            - `faxType` — integer — FAX type
            - `faxSpeed` — integer — FAX speed (available for W04FXO 2020)
            - `codecInputGain` — integer — Adjust incoming audio gain
            - `codecOutputGain` — integer — Adjust outgoing audio gain
            - `preversalDetection` — boolean — Polarity reversal on answer (available for W04FXO R3). Enable/ disable this parameter as the cause for disconnecting the call
  - `type` — string _(default=result)_
- Errors: `401`, `403`

#### `PUT` `/Trunks/Fxo/{id}/`

**Update FXO trunk**

Update FXO trunk by ID

- operationId: `PutTrunksFXO`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Trunk ID
- **Request body** (`application/json`)
  - `username` — string **(required)** — Trunk name
  - `title` — string **(required)** — Trunk title
  - `technology` — string **(required)** — Trunk technology
  - `address` — string **(required)** — IP device address
  - `model` — string **(required)** — Model device
  - `settingsMgw` — object **(required)** — Trunk MGW settings
    - `toneZone` — string — Default Tone Zone
    - `countryCode` — integer — Country Code
    - `isoCode` — string — ISO 3166 country code
    - `impedance` — integer — Impedance values to avoid noise during line connection
    - `dcImpedance` — boolean — DC Impedance (disabled by default)
    - `fskCidField` — string — Obtain FSK CID (available for W04FXO 2020), value to display the correct Caller ID
    - `busyToneDetected` — boolean — Disconnect signaling - busy tone (available for W04FXO R3)
    - `polarityNormalDetected` — boolean — Disconnect signaling - polarity reversal (available for W04FXO R3). This parameter to avoid dropped calls due to a wrong detection of polarity change on the copper line
    - `currentDetected` — boolean — Disconnect signaling - open switching interval (available for W04FXO R3)
    - `currentDisconnectThreshold` — integer — Current Disconnect Threshold in ms
    - `silenceDetectionEnabled` — boolean — Silence detection (available for W04FXO R3). Enable/ disable this parameter as the cause for disconnecting the call
    - `silenceDetection` — integer — Silence detection timeout in second (available for W04FXO R3)
    - `ports` — object — Device ports
      - `port` — integer — number of port
      - `priceList` — integer — The pricelist to calculate the costs for calls through the trunk
      - `destinationCode` — string — Specify the area code
      - `context` — string — Dialplan procedure for routing calls coming from this trunk
      - `hotlineNumber` — string — The number corresponding to the line which is present in the associated Dialplan procedure
      - `pstnRingCount` — boolean — Detect caller ID (available for W04FXO 2020). Enable/disable caller ID detection
      - `cidType` — integer — Caller ID type (available for W04FXO 2020). The standard for transmitting the caller ID information
      - `flashTime` — integer — Flash time (available for FXO gateways pre 2020). Timeout (in msec) for hookflash detection
      - `answerTime` — integer — Dialing answer delay time. Interdigit dial timeout (in sec), when terminated, the call is sent to trunk
      - `faxType` — integer — FAX type
      - `faxSpeed` — integer — FAX speed (available for W04FXO 2020)
      - `codecInputGain` — integer — Adjust incoming audio gain
      - `codecOutputGain` — integer — Adjust outgoing audio gain
      - `preversalDetection` — boolean — Polarity reversal on answer (available for W04FXO R3). Enable/ disable this parameter as the cause for disconnecting the call
- **Response 200** (`ApiResponseSuccess`)
  - `type` — string _(enum: `result`)_
  - `result` — string _(enum: `Success`)_
- Errors: `400`, `401`, `403`, `404`

### Trunks Price

#### `GET` `/Trunks/Prices/`

**Get trunk price list**

Returns trunks price list

- operationId: `getTrunkPrices`
- **Scopes**: `trunks:read`, `pbx:read`
- **Company API Key scope**: `trunks:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — integer — Trunk ID
        - `name` — string — Trunk name.
        - `items` — array
          - _array of_ `object`
            - `dialprefix` — integer — Dial prefix
            - `destination` — integer — Destination
            - `rate` — integer — Rate
            - `minDuration` — integer — Minimum Duration
            - `billingBlock` — integer — Billing block
            - `connectCharge` — integer — Connect charge
            - `startDay` — integer — Start day of week
            - `stopDay` — integer — End day of week
            - `startTime` — integer — Start time
            - `stopTime` — integer — Stop time
- Errors: `401`, `403`

#### `POST` `/Trunks/Prices/`

**Create trunk price list**

Create a file with trunks cost

- operationId: `createPriceById`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — integer — Trunk ID
    - `name` — string — Trunk name.
    - `items` — array
      - _array of_ `object`
        - `dialprefix` — integer — Dial prefix
        - `destination` — integer — Destination
        - `rate` — integer — Rate
        - `minDuration` — integer — Minimum Duration
        - `billingBlock` — integer — Billing block
        - `connectCharge` — integer — Connect charge
        - `startDay` — integer — Start day of week
        - `stopDay` — integer — End day of week
        - `startTime` — integer — Start time
        - `stopTime` — integer — Stop time
- Errors: `400`, `401`, `403`

#### `GET` `/Trunks/Prices/{ID}/export`

**Export trunk price list by ID**

Export price by ID of trunks cost

- operationId: `exportPriceById`
- **Scopes**: `trunks:read`, `pbx:read`
- **Company API Key scope**: `trunks:read`
- **Parameters**
  - `id` (path) — integer **(required)** — Price list ID
- **Response 200**
  - string _(format=binary)_
- Errors: `401`, `403`, `404`

#### `POST` `/Trunks/Prices/{ID}/`

**Update trunk price list by ID**

Update trunks cost by price list ID

- operationId: `updatePriceById`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Price list ID
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — object
    - `id` — integer — Trunk ID
    - `name` — string — Trunk name.
    - `items` — array
      - _array of_ `object`
        - `dialprefix` — integer — Dial prefix
        - `destination` — integer — Destination
        - `rate` — integer — Rate
        - `minDuration` — integer — Minimum Duration
        - `billingBlock` — integer — Billing block
        - `connectCharge` — integer — Connect charge
        - `startDay` — integer — Start day of week
        - `stopDay` — integer — End day of week
        - `startTime` — integer — Start time
        - `stopTime` — integer — Stop time
- Errors: `400`, `401`, `403`, `404`

#### `DELETE` `/Trunks/Prices/{ID}/`

**Delete trunk price list by ID**

Delete price list by ID

- operationId: `deletePriceById`
- **Scopes**: `trunks:*`, `pbx:*`
- **Company API Key scope**: `trunks:*`
- **Parameters**
  - `id` (path) — integer **(required)** — Price list ID
- **Response 200**
  - `type` — string _(default=result)_
  - `result` — string _(default=Success)_
- Errors: `401`, `403`, `404`

### Departments

#### `GET` `/Departments/`

**Get departments**

Returns departments as tree

- operationId: `getDepartments`
- **Scopes**: `info:read`, `pbx:read`
- **Company API Key scope**: `info:read`
- **Response 200**
  - `result` — object
    - `records` — array
      - _array of_ `object`
        - `id` — string — Category id
        - `name` — string — Category name
        - `users` — array — Array of users extensions
          - _array of_ `string`
        - `items` — array — Child elements
          - _array of_ `DepartmentsCategory`
            - `id` — string — Category id
            - `name` — string — Category name
            - `users` — array — Array of users extensions
              - _array of_ `string`
            - `items` — array — Child elements
              - _(nesting depth limit — see `DepartmentsCategory` in the Schemas appendix)_
  - `type` — string _(default=result)_
- Errors: `401`, `403`

### License

#### `GET` `/PBX/settings/license/`

**Get licenses info**

Returns information about licenses
****Available only for administrators with enabled ACL permissions****

- operationId: `getLicenses`
- **Response 200**
  - `result` — object
    - `limitations` — object — Info about limitations
      - `phones` — string — Phones
      - `trunks` — integer — Trunks
      - `calls` — string — Calls
      - `rooms` — string — Rooms
      - `licenseTypes` — LicenseTypes
        - `basic` — integer
        - `essential` — integer
        - `business` — integer
        - `wizyconf` — integer
        - `pbxService` — integer
        - `x-caracal` — integer
        - `classound` — integer
        - `msphonesystem` — integer
      - `faxes` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `redundancy` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `perUser` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `support` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `cloud` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `cti_cdr_view` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `cti_connect_pro` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `cti_operator_panel` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `hotel` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `tapi` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `cti_conference` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `upgrade_2.0_3.0` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `license_update` — LimitationItem
        - `state` — boolean
        - `until` — string
      - `serial` — string
      - `networkLicense` — integer
      - `x-bees` — integer
    - `licenseUsage` — LicenseTypes
      - `basic` — integer
      - `essential` — integer
      - `business` — integer
      - `wizyconf` — integer
      - `pbxService` — integer
      - `x-caracal` — integer
      - `classound` — integer
      - `msphonesystem` — integer
    - `activated` — boolean — Is PBX activated
    - `hwserial` — string — Hardware serial
    - `swserial` — string — Hardware serial
    - `domain` — string — PBX domain
    - `processor` — string — PBX processor
    - `memory` — integer — PBX memory
    - `logoExist` — boolean — Flag is exist logo
  - `type` — string _(default=result)_
- Errors: `401`, `403`

### Broadcasts

#### `POST` `/broadcasts/reload/`

**Reload broadcasts**

- operationId: `reloadBroadcasts`
- **Response 200**
  - `type` — string _(enum: `result`)_
  - `result` — string _(default=broadcasts have been updated)_
- Errors: `401`, `403`, `500`

### Call Control

#### `POST` `/call-control/make-call/`

**Initiate a new call**

Initiate a new outbound call from the specified user to the destination.

**Access Control:**
- Root admin can specify any user extension via query parameter
- Regular users can only make calls from their own extension

**Device Selection:**
- If no deviceContact is provided, the user's active device will be used automatically
- If no callType is specified, defaults to 'device' type

- operationId: `makeCall`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Parameters**
  - `user` (query) — string — User extension (only for root admins)
- **Request body** (`application/json`) **(required)**
  - `destination` — string **(required)** — Destination number or extension
  - `callType` — string — Type of call _(default=device; enum: `any`, `mobility`, `device`)_
  - `deviceContact` — string — Device contact URI (if not provided, uses user's active device)
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `503`

#### `POST` `/call-control/answer/`

**Answer an incoming call**

Answer an incoming call using the specified call ID

- operationId: `answerCall`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP call identifier
  - `deviceContact` — string — Device contact URI
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `503`

#### `POST` `/call-control/hold/`

**Put a call on hold**

Put the specified call on hold

- operationId: `holdCall`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP call identifier
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `503`

#### `POST` `/call-control/unhold/`

**Resume a call from hold**

Resume the specified call from hold

- operationId: `unholdCall`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP call identifier
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `503`

#### `POST` `/call-control/blind-transfer/`

**Perform a blind transfer**

Transfer a call directly to another destination without consultation.
The destination can be an extension number, phone number.

**Access Control:**
- Root admin can specify any user extension via query parameter
- Regular users can only transfer their own calls

- operationId: `blindTransferCall`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Parameters**
  - `user` (query) — string — User extension (only for root admins)
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP call identifier of the call to transfer
  - `destination` — string **(required)** — Transfer destination (extension, phone number)
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `503`

#### `POST` `/call-control/attendant-transfer/`

**Perform an attendant transfer**

Transfer a call to another active call (consultation transfer).
The destination should be the SIP call ID of another active call

- operationId: `attendantTransferCall`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP call identifier of the call to transfer
  - `destination` — string **(required)** — SIP call identifier of the target call
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `503`

#### `POST` `/call-control/dtmf/`

**Send DTMF to a call**

Send DTMF to the specified call

- operationId: `sendDtmf`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP call identifier
  - `digits` — string **(required)** — Digits to send _(minLen=1; maxLen=10)_
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `404`, `503`

#### `POST` `/call-control/hangup/`

**End a call**

Terminate the specified active call

- operationId: `hangupCall`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — SIP call identifier
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `503`

#### `GET` `/call-control/list-devices/`

**List registered devices**

Get a list of registered devices for an extension.

**Access Control:**
- Root admin can query any extension by providing the 'user' parameter
- Regular users can only query their own devices

- operationId: `listDevices`
- **Scopes**: `callcontrol:read`, `pbx:read`
- **Company API Key scope**: `callcontrol:read`
- **Parameters**
  - `user` (query) — string — Extension to query (only for root admin)
- **Response 200**
  - `devices` — array
    - _array of_ `object`
      - `userAgent` — string
      - `contact` — string
      - `active` — boolean — Whether this device is currently selected as active device
- Errors: `400`, `403`, `500`

#### `PUT` `/call-control/set-active-device/`

**Set active device for calling**

Set which device should be used for outgoing calls.

**Device Types:**
- device: Specific physical device (requires contact and userAgent)
- mobility: Mobile/forwarding mode
- any: Ring all devices

**Access Control:**
- Authenticated users can set their own active device
- Root admin can set active device for other users (with 'user' parameter)

**Note:** The device user agent must match the pattern supported by Kamailio
(e.g., Wildix WP, Zero Distance, Android, iOS, Vision, SuperVision, Web, etc.)

- operationId: `setActiveDevice`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Parameters**
  - `user` (query) — string — Extension (only for root admin)
- **Request body** (`application/json`) **(required)**
  - _oneOf_ — exactly one of:
    - **`Physical Device`**
      - `deviceType` — string **(required)** — Physical device type _(enum: `device`)_
      - `contact` — string **(required)** — SIP contact URI _(pattern=^sip:)_
      - `userAgent` — string **(required)** — Device user agent (must be a Wildix device)
      - `user` — string — Extension (only for root admin)
    - **`Mobility Mode`**
      - `deviceType` — string **(required)** — Mobile/forwarding mode _(enum: `mobility`)_
      - `user` — string — Extension (only for root admin)
    - **`Ring All Devices`**
      - `deviceType` — string **(required)** — Ring all registered devices _(enum: `any`)_
      - `user` — string — Extension (only for root admin)
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `404`

#### `GET` `/call-control/list-calls/`

**List active calls**

Get a list of active calls for an extension.

**Access Control:**
- Root admin can query any extension by providing the 'user' parameter
- Regular users can only query their own calls

- operationId: `listCalls`
- **Scopes**: `callcontrol:read`, `pbx:read`
- **Company API Key scope**: `callcontrol:read`
- **Parameters**
  - `user` (query) — string — Extension to query (only for root admin)
- **Response 200**
  - `calls` — array
    - _array of_ `object`
      - `sipCallId` — string
      - `callerNumber` — string
      - `callerName` — string
      - `calleeNumber` — string
      - `calleeName` — string
      - `state` — string
      - `duration` — integer — Call duration in seconds
  - `total` — integer — Total number of active calls
- Errors: `400`, `403`, `503`

#### `POST` `/call-control/update-contact-info/`

**Update contact information for an active call**

Updates the name and/or number displayed for a specific call.

**Access Control:**
- Root admin can update any call
- Regular users can only update their own calls

- operationId: `updateContactInfo`
- **Scopes**: `callcontrol:*`, `pbx:*`
- **Company API Key scope**: `callcontrol:*`
- **Request body** (`application/json`) **(required)**
  - `sipCallId` — string **(required)** — Unique ID of the call to update
  - `name` — string — New name to display (optional if number is provided)
  - `number` — string — New number to display (optional if name is provided)
- **Response 200**
  - `message` — string
- Errors: `400`, `403`, `404`, `503`

### UserFeatures

#### `GET` `/api/v2/personal/features`

**Get user personal features**

Retrieve personal features and settings for the authenticated user or specified user. Includes available ringtones and other user-specific configurations.

- operationId: `getUserFeatures`
- **Parameters**
  - `uid` (query) — string — User ID to get features for. If not provided, returns features for the authenticated user. Requires appropriate permissions to access other users' features.
  - `fields` (query) — string — Comma-separated list of specific feature fields to retrieve. If empty, returns all available features including ringtones.
- **Response 200**
  - `success` — boolean
  - `result` — object — User features object containing requested fields
    - `ringtones` — object — Available ringtones organized by directory path
      - _map of_ `array`
        - _array of_ `string`
    - `callForwarding` — object — Call forwarding settings
    - `voicemail` — object — Voicemail settings
- Errors: `400`, `401`, `403`, `500`

#### `POST` `/api/v2/personal/features`

**Update user personal features**

Update personal features and settings for the authenticated user or specified users. Supports bulk operations with comma-separated user IDs. Note that ringtones are read-only and cannot be modified via this endpoint.

- operationId: `setUserFeatures`
- **Parameters**
  - `uid` (query) — string — User ID(s) to update features for. Can be comma-separated for bulk operations. If not provided, updates features for the authenticated user. Requires appropriate permissions for other users.
- **Request body** (`application/json`) **(required)**
- **Response 200**
  - _oneOf_ — exactly one of:
    - **`object`**
      - `success` — boolean
      - `result` — boolean
    - **`object`**
      - `success` — boolean
      - `result` — object — Results for each user ID
        - _map of_ `object`
          - `success` — boolean
          - `error` — string
- Errors: `400`, `401`, `403`, `500`

### Schemas appendix — PBX API

<details><summary>55 component schemas</summary>

**`ActiveCall`**

- `callid` — string — Unique call identifier
- `caller_id_num` — string — Caller ID number
- `caller_id_name` — string — Caller ID name
- `connected_line_num` — string — Connected line number
- `connected_line_name` — string — Connected line name
- `state` — string — Current call state _(enum: `Down`, `Rsrvd`, `OffHook`, `Dialing`, `Ring`, `Ringing`, `Up`, `Busy`, `Dialing Offhook`, `Pre-ring`)_
- `duration` — string — Call duration in seconds

**`AnswerCallRequest`**

- `callid` — string **(required)** — The unique identifier of the call to answer
- `device_contact` — string — Optional. Device contact information for the specific device to answer the call

**`ApiResponseBadRequest`**

- `type` — string _(enum: `error`)_
- `result` — any
- `reason` — string _(enum: `BadRequest`, `Validation error`)_
- `code` — string _(enum: `BadRequest`)_
- `errors` — object
  - `parameter1` — object
    - `code` — string
    - `reason` — string
  - `parameter2` — object
    - `code` — string
    - `reason` — string
  - `parameterN` — object
    - `code` — string
    - `reason` — string

**`ApiResponseColleague`**

- `type` — string **(required)** _(enum: `result`)_
- `result` — object **(required)**
  - `id` — string
  - `dn` — string _(minLen=4)_
  - `pbxDn` — string _(minLen=4)_
  - `jid` — string _(format=email)_
  - `extension` — string — A numeric string _(minLen=2; maxLen=50)_
  - `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
  - `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
  - `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
  - `email` — string _(format=email)_
  - `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
  - `groupDn` — string _(minLen=4)_
  - `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
  - `dialplan` — string
  - `faxDialplan` — string
  - `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
  - `login` — string — A string without special chars _(minLen=2; maxLen=50)_
  - `picture` — string
  - `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
  - `groupName` — string — Group name

**`ApiResponseColleagueNotFound`**

- `type` — string _(enum: `error`)_
- `reason` — string
- `result` — any
- `code` — string

**`ApiResponseError`**

- `type` — string _(enum: `error`)_
- `reason` — string
- `result` — any
- `code` — any

**`ApiResponseForbidden`**

- `type` — string _(enum: `error`)_
- `reason` — string _(enum: `Access error`)_
- `result` — any
- `code` — string _(enum: `AccessError`)_

**`ApiResponseItemNotFound`**

- `type` — string _(enum: `error`)_
- `reason` — string
- `result` — any
- `code` — string

**`ApiResponseNotFound`**

- `type` — string _(enum: `error`)_
- `reason` — string
- `result` — any
- `code` — string

**`ApiResponseNotFound2`**

- `type` — string _(enum: `error`)_
- `reason` — string
- `result` — any
- `code` — string

**`ApiResponseSipRegistrations`**

- `type` — string **(required)** _(enum: `result`)_
- `result` — object **(required)**

**`ApiResponseSuccess`**

- `type` — string _(enum: `result`)_
- `result` — string _(enum: `Success`)_

**`ApiResponseTrue`**

- `type` — string _(enum: `result`)_
- `result` — boolean _(enum: `True`)_

**`ApiResponseUnauthorized`**

- `type` — string _(enum: `error`)_
- `result` — any
- `reason` — string _(enum: `Unauthorized`)_

**`ApplicationItem`**

- `id` — string — Application ID
- `app` — string — Application name
- `secret` — string — Secret key
- `pbxUser` — string — PBX user (login or extension)
- `created` — integer — Application created timestamp
- `expireTime` — integer — Token expiration timestamp (Unix timestamp)

**`ApplicationItem2`**

- `id` — string — Application ID
- `name` — string — Application name
- `secret` — string — Secret key
- `accessTokenTtl` — integer — Lifetime of the access token
- `created` — integer — Application created timestamp
- `expireTime` — integer — Token expiration timestamp (Unix timestamp)
- `redirectUri` — array — List of redirect URIs
  - _array of_ `any`

**`ApplicationItem3`**

- `id` — string — Application ID
- `name` — string — Application name
- `secret` — string — Secret key
- `pbxUser` — string — PBX user (login or extension)
- `created` — integer — Application created timestamp
- `expireTime` — integer — Token expiration timestamp (Unix timestamp)

**`AttendantTransferRequest`**

- `callid` — string **(required)** — The unique identifier of the first call to transfer
- `second_callid` — string **(required)** — The unique identifier of the second call to connect

**`BlindTransferRequest`**

- `callid` — string **(required)** — The unique identifier of the call to transfer
- `destination` — string **(required)** — The destination number to transfer the call to

**`CallControlSuccessResponse`**

- `type` — string _(enum: `result`)_
- `result` — object
  - `message` — string — Success message describing the operation result

**`CallGroupItemEdit`**

- `title` — string — Call group name
- `members` — array — Members array
  - _array of_ `any`
- `settings` — object — Group settings
  - `queueManager` — string — Missed calls managers
  - `cid` — string — CID for outbound calls
  - `autoPause` — string — Auto pause on no answer _(default=False; enum: `False`, `True`, `all`)_
  - `autoPauseTime` — integer — Auto pause on no answer timeout _(default=5)_
  - `autoPauseDelay` — integer — Auto pause delay _(default=0)_
  - `maxLen` — integer — Max length _(default=5)_
  - `retry` — integer — Seconds before recalling all the members again _(default=1)_
  - `ringInUse` — boolean — Call waiting _(default=False)_
  - `strategy` — string — Strategy _(default=ringall; enum: `ringall`, `roundrobin`, `wringall`, `leastrecent`, `fewestcalls`, `linear`)_
  - `timeout` — integer — Timeout (0 - 120) _(default=60)_
  - `weight` — integer — Priority _(default=0)_
  - `wrapUpTime` — integer — Wrap up time _(default=0)_
  - `rule` — string — Dialplan
  - `broadcast` — string — Broadcast channel to handle calls. Required if Broadcast Skills provided. Applies only for x-hoppers license.
  - `broadcastSkills` — string — List of skills separated by comma. Requires broadcast to be provided. Applies only for x-hoppers license.
  - `broadcastPriority` — integer — Set the priority level for handling broadcast calls. Applies only for x-hoppers license. _(default=0)_
  - `announce` — object
    - `frequency` — integer — Announce frequency _(default=0)_
    - `holdTime` — string — Announce hold time _(default=True; enum: `True`, `False`, `once`)_
  - `exitAllMembers` — object
    - `busy` — boolean — Exit if all members busy _(default=False)_
    - `paused` — boolean — Exit if all members paused / wrap up _(default=False)_
    - `ringing` — boolean — Exit if all members ringing _(default=False)_
  - `aclGroup` — integer — GID of the ACL group linked to this call group. Users with the `MANAGE_CALLGROUP` permission granted on this ACL group are authorized to manage the call group.

**`CallHistory`**

- `type` — string **(required)** _(enum: `result`)_
- `result` — object **(required)**
  - `total` — integer **(required)**
  - `records` — array **(required)**
    - _array of_ `object`
      - `id` — string
      - `start` — string
      - `answer` — string
      - `end` — string
      - `src` — string
      - `dst` — string
      - `from_number` — string
      - `to_number` — string
      - `from_name` — string
      - `to_name` — string
      - `billsec` — string
      - `disposition` — string _(enum: `NO ANSWER`, `ANSWERED`, `BUSY`)_
      - `lastapp` — string
      - `userfield` — string
      - `faxdata` — string
      - `lastdata` — string
      - `cost` — string
      - `organization` — string
      - `channel` — string
      - `dstchannel` — string
      - `app` — string
      - `callclass` — string
      - `dest_type` — string
      - `duration` — string
      - `dcontext` — string
      - `pbxid` — string
      - `type` — string _(enum: `call`, `fax`, `voicemail`)_
      - `attachments` — object — Voice mail, recordings, faxes info
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `timezone` — string **(required)**

**`Colleague`**

- `id` — string
- `dn` — string _(minLen=4)_
- `pbxDn` — string _(minLen=4)_
- `jid` — string _(format=email)_
- `extension` — string — A numeric string _(minLen=2; maxLen=50)_
- `name` — string — A string. Allowed special chars: "-", "_" _(minLen=2; maxLen=50)_
- `sourceId` — string — A string without special chars _(minLen=2; maxLen=50)_
- `officePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
- `mobilePhone` — string — A valid phone number _(minLen=2; maxLen=50)_
- `faxNumber` — string — A valid phone number _(minLen=2; maxLen=50)_
- `email` — string _(format=email)_
- `role` — string _(enum: `admin`, `user`, `fax`, `park_orbit`, `room`)_
- `groupDn` — string _(minLen=4)_
- `language` — string — A language code. Example: en, it, fr, de, ru, bg, es, nl, en-us, ee _(minLen=2; maxLen=5)_
- `dialplan` — string
- `faxDialplan` — string
- `department` — string — A string without special chars: "@", "&", ">", "<" _(minLen=1; maxLen=250)_
- `login` — string — A string without special chars _(minLen=2; maxLen=50)_
- `picture` — string
- `licenseType` — string _(enum: `basic`, `essential`, `business`, `premium`, `wizyconf`)_
- `groupName` — string — Group name

**`CorrectKeys`**

- string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_

**`DepartmentsCategory`**

- `id` — string — Category id
- `name` — string — Category name
- `users` — array — Array of users extensions
  - _array of_ `string`
- `items` — array — Child elements
  - _array of_ `DepartmentsCategory`
    - _(nesting depth limit — see `DepartmentsCategory` in the Schemas appendix)_

**`DialplanItem`**

- `id` — integer — Dialplan ID
- `name` — string — Dialplan name
- `description` — string — Dialplan description
- `numbers` — array — List of numbers
  - _array of_ `object`
    - `number` — string — Rule number
    - `apps` — array — List of rules
      - _array of_ `object`
        - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `comment` — string — Comment
- `includedDialplans` — array — List of included Dialplans (can be empty)
  - _array of_ `object`
    - `dialplanId` — integer — Dialplan ID. Allowed numbers greater or less zero

**`DialplanItemIncludes`**

- `dialplanId` — integer — Dialplan ID. Allowed numbers greater or less zero

**`DialplanItemNumber`**

- `number` — string — Rule number
- `apps` — array — List of rules
  - _array of_ `object`
    - `name` — string — Application name (key) https://wildix.atlassian.net/wiki/x/ahDOAQ _(enum: `Answer`, `AsrIvr`, `AuthenticateUser`, `Background`, `Callback`, `Conference`, `CorrectOutgoingNumber`, `CustomApp`, `DialHuntGroup`, `DialPhone`, `DialRemotePbx`, `DialTrunk`, … (+30))_
    - `params` — object — List of application params (allowed empty)
      - `key_1` — string — value 1
      - `key_2` — string — value 2
      - `key_N` — string — value N
- `comment` — string — Comment

**`Errors`**

- `parameter1` — object
  - `code` — string
  - `reason` — string
- `parameter2` — object
  - `code` — string
  - `reason` — string
- `parameterN` — object
  - `code` — string
  - `reason` — string

**`HangupCallRequest`**

- `callid` — string **(required)** — The unique identifier of the call to hangup

**`HoldCallRequest`**

- `callid` — string **(required)** — The unique identifier of the call to hold

**`HttpProxyItem`**

- `enable` — boolean — Enable HTTP proxy for Support VPN
- `host` — string — Proxy host
- `port` — string — Port
- `auth_method` — string — Proxy authentication method _(default=none; enum: `none`, `basic`, `ntlm`)_
- `login` — string — Login
- `password` — string — Password

**`IvrChildAction`**

- `number` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
- `type` — string — Tree node type _(default=item)_
- `parameters` — object — Item parameters
  - `context` — string — Dialplan procedure
  - `exten` — string — Called number

**`IvrChildMenu`**

- `number` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
- `type` — string — Tree node type _(default=menu)_
- `parameters` — MenuParameters — Menu parameters
  - `sound` — string **(required)** — Path to sound file
  - `times` — integer **(required)** — Number of times the audio file is played back to the caller
  - `timeout` — integer **(required)** — After this timeout in seconds, the Timeout action is performed
  - `backcode` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
  - `context` — string — Dialplan procedure
  - `exten` — string — Called number
- `items` — array — Child elements (menu or item)
  - _array of_ `union`
    - _anyOf_ — one or more of:
      - **`IvrChildMenu`**
        - _(nesting depth limit — see `IvrChildMenu` in the Schemas appendix)_
      - **`IvrChildAction`**
        - `number` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
        - `type` — string — Tree node type _(default=item)_
        - `parameters` — object — Item parameters
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`IvrRoot`**

- `id` — integer — IVR ID
- `title` — string — IVR name
- `type` — string — Tree node type (menu or action) _(enum: `menu`, `item`)_
- `parameters` — object — Menu parameters
  - `sound` — string **(required)** — Path to sound file
  - `times` — integer **(required)** — Number of times the audio file is played back to the caller
  - `timeout` — integer **(required)** — After this timeout in seconds, the Timeout action is performed
  - `backcode` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
  - `context` — string — Dialplan procedure
  - `exten` — string — Called number
- `items` — array — Child elements (menu or item)
  - _array of_ `union`
    - _anyOf_ — one or more of:
      - **`Menu node`**
        - `number` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
        - `type` — string — Tree node type _(default=menu)_
        - `parameters` — MenuParameters — Menu parameters
          - _(nesting depth limit — see `MenuParameters` in the Schemas appendix)_
        - `items` — array — Child elements (menu or item)
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - **`Action node`**
        - `number` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
        - `type` — string — Tree node type _(default=item)_
        - `parameters` — object — Item parameters
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_

**`LicenseTypes`**

- `basic` — integer
- `essential` — integer
- `business` — integer
- `wizyconf` — integer
- `pbxService` — integer
- `x-caracal` — integer
- `classound` — integer
- `msphonesystem` — integer

**`LimitationItem`**

- `state` — boolean
- `until` — string

**`ListCallsRequest`**

- `extension` — string **(required)** — Extension number to list calls for

**`ListCallsResponse`**

- `type` — string _(enum: `result`)_
- `result` — object
  - `calls` — array — List of active calls
    - _array of_ `ActiveCall`
      - `callid` — string — Unique call identifier
      - `caller_id_num` — string — Caller ID number
      - `caller_id_name` — string — Caller ID name
      - `connected_line_num` — string — Connected line number
      - `connected_line_name` — string — Connected line name
      - `state` — string — Current call state _(enum: `Down`, `Rsrvd`, `OffHook`, `Dialing`, `Ring`, `Ringing`, `Up`, `Busy`, `Dialing Offhook`, `Pre-ring`)_
      - `duration` — string — Call duration in seconds

**`ListDevicesRequest`**

- `extension` — string **(required)** — Extension number to list devices for

**`ListDevicesResponse`**

- `type` — string _(enum: `result`)_
- `result` — object
  - `devices` — array — List of registered devices
    - _array of_ `object`
      - `user_agent` — string — Device user agent string
      - `contact` — string — Device contact information
  - `active_device` — object — Currently active device information
    - `contact` — string — Device contact information
    - `user_agent` — string — Device user agent string

**`MakeCallRequest`**

- `user` — string — The extension number of the user
- `destination` — string **(required)** — The destination number to call
- `call_type` — string — Optional. Type of call (any | mobility | device). Defaults to "any" if not specified. _(default=any; enum: `any`, `mobility`, `device`)_
- `device_contact` — string — Optional. Device contact, specified if the type of call device. If not present, kamailio will add this param from device selected by user

**`MenuParameters`**

_Menu parameters_

- `sound` — string **(required)** — Path to sound file
- `times` — integer **(required)** — Number of times the audio file is played back to the caller
- `timeout` — integer **(required)** — After this timeout in seconds, the Timeout action is performed
- `backcode` — string _(enum: `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `0`, `*`, … (+1))_
- `context` — string — Dialplan procedure
- `exten` — string — Called number

**`SmtpItem`**

- `account` — string — SMTP account _(default=default)_
- `auth` — string — SMTP server auth type _(enum: `False`, `True`, `login`, `plain`, `cram-md5`, `digest-md5`, `gssapi`, `ntlm`)_
- `host` — string — SMTP server host
- `from` — string — From field in the email
- `port` — integer — SMTP server port number
- `timeout` — integer — SMTP server timeout for sending email _(enum: `2`, `5`, `10`, `15`, `20`, `60`)_
- `user` — string — SMTP user name
- `password` — string — SMTP user password
- `domain` — string — HELO Domain
- `tls` — boolean — Enable TLS for the secure connection
- `tlsStartTls` — boolean — Enable STARTTLS to start TLS encryption
- `isDefaultSettings` — boolean — Enable default SMTP settings (for Cloud PBX only)

**`TimeTables`**

- `id` — integer — Timetable ID
- `title` — string — Timetable name
- `state` — integer — Timetable state
- `items` — object
  - `month` — integer — Mouth number.
  - `year` — integer — Year.
  - `from` — object
    - `day` — integer — Start day of month
    - `dayOfWeek` — integer — Start day of week
  - `to` — object
    - `day` — integer — End day of month
    - `dayOfWeek` — integer — End day of week
  - `time` — object
    - `from` — string — Start time
    - `to` — string — End time

**`TransferCallRequest`**

- _oneOf_ — exactly one of:
  - **`BlindTransferRequest`**
    - `callid` — string **(required)** — The unique identifier of the call to transfer
    - `destination` — string **(required)** — The destination number to transfer the call to
  - **`AttendantTransferRequest`**
    - `callid` — string **(required)** — The unique identifier of the first call to transfer
    - `second_callid` — string **(required)** — The unique identifier of the second call to connect

**`UnholdCallRequest`**

- `callid` — string **(required)** — The unique identifier of the call to unhold

**`UpgradeSettings`**

- `wmsrelease` — object — WMS release section
  - `repository` — string — Upgrade repository _(default=rel50; enum: `rel50`, `rel50dev`, `rel50alpha`, `rel50beta`, `rel50test`)_
  - `enabled` — boolean — Enable PBX auto upgrade
  - `email` — string — Email for sending backup and upgrade log
  - `howly` — string — Interval for checking auto upgrade _(enum: `daily`, `weekly`, `monthly`)_
- `customFirmwareServer` — object — Custom firmware server section
  - `url` — string — Custom firmware server URL (required if enabled)
  - `enabled` — boolean — Enable custom firmware server
  - `checkTls` — boolean — Check SSL/TLS Certificate for server

**`changeRoom`**

- `subject` — string **(required)** — Conference title
- `participants` — array — Conference participants
  - _array of_ `object`
    - `type` — string **(required)** — Type of a participant. Colleague or email invitee _(enum: `colleague`, `email`)_
    - `name` — string **(required)** — Participant name
    - `jid` — string **(required)** — Participant JID. **Required if "type" is "colleague"**
    - `email` — string **(required)** — Participant email. **Required if "type" is "email"**
- `schedule` — object — Conference schedule
  - `enabled` — boolean **(required)** — Enable or disable the schedule
  - `start` — string **(required)** — Conference start date and time. **Required if "enabled" is "true"**
  - `end` — string **(required)** — Conference start date and time. **Required if "enabled" is "true"**
  - `timezone` — string **(required)** — The IANA time zone identifier. **Required if "enabled" is "true"**
  - `recurrence` — string — Conference frequency. String in RRULE RFC 5454 Examples: * *FREQ=DAILY;INTERVAL=1* - repeat every day * *FREQ=WEEKLY;INTERVAL=1;BYDAY=MO,TU;UNTIL=20230531T000000Z* - repeat every week on Monday and Tuesday until May 31, 2023 * *FREQ=WEEKLY;INTERVAL=1;BYDAY=MO;COUNT=10* - repeat every week on Mondays 10 times
  - `description` — string — Conference description
  - `country` — string — Two-letter ISO 3166 country code
  - `lang` — string — Two-letter language code _(default=en)_
  - `dialInNumbers` — array — Two-letter country codes for connecting to a phone conference in these countries. _(default=['gb'])_
    - _array of_ `string`
- `password` — string — Conference password _(minLen=6; maxLen=10)_

**`featureStatusStructure`**

- `_ACTIVATED` — object
  - `status` — string
- `MEXT` — object
  - `status` — string
  - `value` — string
- `BCF` — object
  - `status` — string
  - `value` — string
- `UCF` — object
  - `status` — string
  - `value` — string
- `SMSMCN` — object
  - `status` — string
- `REJECT` — object
  - `status` — string
- `EMAILMCN` — object
  - `status` — string
- `FCF` — object
  - `status` — string
  - `value` — string
- `TOUT` — object
  - `status` — string
  - `value` — string
- `CW` — object
  - `status` — string
- `MOBCONFIRMATION` — object
  - `status` — string
- `RING` — object
  - `status` — string
  - `value` — string

**`featureType`**

- `away` — object
  - `_ACTIVATED` — object
    - `status` — string
  - `MEXT` — object
    - `status` — string
    - `value` — string
  - `BCF` — object
    - `status` — string
    - `value` — string
  - `UCF` — object
    - `status` — string
    - `value` — string
  - `SMSMCN` — object
    - `status` — string
  - `REJECT` — object
    - `status` — string
  - `EMAILMCN` — object
    - `status` — string
  - `FCF` — object
    - `status` — string
    - `value` — string
  - `TOUT` — object
    - `status` — string
    - `value` — string
  - `CW` — object
    - `status` — string
  - `MOBCONFIRMATION` — object
    - `status` — string
  - `RING` — object
    - `status` — string
    - `value` — string
- `dnd` — featureStatusStructure
  - `_ACTIVATED` — object
    - `status` — string
  - `MEXT` — object
    - `status` — string
    - `value` — string
  - `BCF` — object
    - `status` — string
    - `value` — string
  - `UCF` — object
    - `status` — string
    - `value` — string
  - `SMSMCN` — object
    - `status` — string
  - `REJECT` — object
    - `status` — string
  - `EMAILMCN` — object
    - `status` — string
  - `FCF` — object
    - `status` — string
    - `value` — string
  - `TOUT` — object
    - `status` — string
    - `value` — string
  - `CW` — object
    - `status` — string
  - `MOBCONFIRMATION` — object
    - `status` — string
  - `RING` — object
    - `status` — string
    - `value` — string
- `default` — featureStatusStructure
  - `_ACTIVATED` — object
    - `status` — string
  - `MEXT` — object
    - `status` — string
    - `value` — string
  - `BCF` — object
    - `status` — string
    - `value` — string
  - `UCF` — object
    - `status` — string
    - `value` — string
  - `SMSMCN` — object
    - `status` — string
  - `REJECT` — object
    - `status` — string
  - `EMAILMCN` — object
    - `status` — string
  - `FCF` — object
    - `status` — string
    - `value` — string
  - `TOUT` — object
    - `status` — string
    - `value` — string
  - `CW` — object
    - `status` — string
  - `MOBCONFIRMATION` — object
    - `status` — string
  - `RING` — object
    - `status` — string
    - `value` — string

**`getRoom`**

- `room` — string — Room ID
- `pin` — string — Conference ID number. Required to connect to a conference with Dial numbers
- `jid` — string — Room JID
- `url` — string — Conference URL
- `subject` — string — Room title
- `owner` — string — Owner JID
- `created` — integer — Timestamp when the room was created
- `visited` — integer — Timestamp when the room was visited
- `online` — boolean — Whether the conference is active
- `occupants` — integer — The number of users who are currently in the conference
- `schedule` — object — Conference schedule
  - `start` — string — Conference start date and time
  - `end` — string — Conference end date and time
  - `recurrence` — string — Conference frequency. String in RRULE RFC 5454
  - `description` — string — Conference description
  - `enabled` — boolean — Enable or disable the schedule
  - `country` — string — Two-letter ISO 3166 country code
  - `timezone` — string — The IANA time zone identifier
  - `lang` — string — Two-letter language code
  - `dialInNumbers` — array — Two-letter country codes for connecting to a phone conference in these countries.
    - _array of_ `string`
- `participants` — object — Conference participants
  - `type` — string — Type of a participant. Colleague or email invitee
  - `name` — string — Participant name
  - `jid` — string — Participant JID
  - `email` — string — Participant email
  - `phone` — string — Participant phone
  - `extension` — string — Participant extension
  - `serial` — string — PBX serial
- `password` — string — Conference password
- `passwordPin` — string — Conference password for HW

**`list`**

- `type` — string _(default=result)_
- `result` — object
  - `rows` — array — List of IPs
    - _array of_ `string`

**`list2`**

- `type` — string _(default=result)_
- `result` — object
  - `total` — int _(default=112)_
  - `records` — array
    - _array of_ `object`
      - `id` — int
      - `email` — string
      - `extension` — string
      - `phone` — string
      - `office` — string
      - `home` — string
      - `home_mobile` — string
      - `fax` — string
      - `mobile` — string
      - `organization` — string
      - `picture` — string
      - `shortcut` — string
      - `phonebook_id` — int
      - `type` — string
      - `note` — string
      - `address` — string
      - `vat_id` — string
      - `name_prefix` — string
      - `document_type` — string
      - `document_id` — string
      - `pin` — string
      - `credit` — string
      - `hash` — string
      - `country` — string
      - `date_birth` — string
      - `born_in` — string
      - `postal_code` — string
      - `city` — string
      - `province` — string
      - `license_plate` — string
      - `document_released` — string
      - `document_from` — string
      - `department` — string
      - `last_update` — string

**`listContactsId`**

- `type` — string _(default=result)_
- `result` — object
  - `id` — int
  - `email` — string
  - `extension` — string
  - `phone` — string
  - `office` — string
  - `home` — string
  - `home_mobile` — string
  - `fax` — string
  - `mobile` — string
  - `organization` — string
  - `picture` — string
  - `shortcut` — string
  - `phonebook_id` — int
  - `type` — string
  - `note` — string
  - `address` — string
  - `vat_id` — string
  - `name_prefix` — string
  - `document_type` — string
  - `document_id` — string
  - `pin` — string
  - `credit` — string
  - `hash` — string
  - `country` — string
  - `date_birth` — string
  - `born_in` — string
  - `postal_code` — string
  - `city` — string
  - `province` — string
  - `license_plate` — string
  - `document_released` — string
  - `document_from` — string
  - `department` — string
  - `last_update` — string

</details>
