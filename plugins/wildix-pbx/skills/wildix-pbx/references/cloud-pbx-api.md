## Cloud PBX API (Permissions)

_OpenAPI: WMS Permissions service — version v1_

**Servers**

- `https://wms-api.wildix.com` — Production
- `https://wms-api-stable.wildix.com` — Stable
- `https://wms-api-stage.wildix.com` — Stage

### CallRecordings

#### `POST` `/v1/permissions/delete_call_recordings_of_users/check` 🆕

Checks the `can: Delete call recordings` permission of a specific user for the participants of a call or conference. Allowed when the user can see call recordings and at least one target is in a group the permission allows. A PBX without the rule denies.

- operationId: `CheckDeleteCallRecordingsOfUsersPermission`
- **Request body** (`application/json` — `CheckDeleteCallRecordingsOfUsersPermissionRequestContent`) **(required)**
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `target` — array **(required)** — The participants of the call (all flows) or conference. Allowed when at least one of them is in an allowed group.
    - _array of_ `Identity`
      - `extension` — string
      - `email` — string
      - `userId` — string
      - `groupId` — string
- **Response 200** (`CheckDeleteCallRecordingsOfUsersPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to delete call recordings, transcriptions and insights of the target.
- Errors: `400`, `403`

#### `POST` `/v1/permissions/see_call_recordings/check`

Checks the `can: See Call Recordings` permissions for a specific user.

- operationId: `CheckSeeCallRecordingsPermission`
- **Request body** (`application/json` — `CheckSeeCallRecordingsPermissionRequestContent`)
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- **Response 200** (`CheckSeeCallRecordingsPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to see call recordings.
- Errors: `400`, `403`

#### `POST` `/v1/permissions/view_call_recordings_of_users/check`

Checks the `can: See call recordings` permissions of a specific user for the list of targets.

- operationId: `CheckViewCallRecordingsOfUsersPermission`
- **Request body** (`application/json` — `CheckViewCallRecordingsOfUsersPermissionRequestContent`) **(required)**
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `target` — array **(required)** — A list of users or groups to check whether action is allowed to perform.
    - _array of_ `Identity`
      - `extension` — string
      - `email` — string
      - `userId` — string
      - `groupId` — string
- **Response 200** (`CheckViewCallRecordingsOfUsersPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to view call recordings against the target.
- Errors: `400`, `403`

#### `POST` `/v1/permissions/view_call_recordings_of_users/groups`

Gets a list of groups that are allowed to see the analytics.

- operationId: `GetViewCallRecordingsOfUsersGroups`
- **Request body** (`application/json` — `GetViewCallRecordingsOfUsersGroupsRequestContent`)
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`GetViewCallRecordingsOfUsersGroupsResponseContent`)
  - `groups` — array **(required)**
    - _array of_ `string`
  - `everybody` — boolean **(required)**
- Errors: `400`, `403`

### Intrusion

#### `POST` `/v1/permissions/intrusion/check`

Checks the `can: Intrusion` permissions for a specific user for the target.

- operationId: `CheckIntrusionPermission`
- **Request body** (`application/json` — `CheckIntrusionPermissionRequestContent`) **(required)**
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `target` — Identity **(required)**
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`CheckIntrusionPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to use instrusion against the target.
- Errors: `400`, `403`

#### `POST` `/v1/permissions/intrusion/groups`

Gets a list of groups that are allowed to use the intrusion.

- operationId: `GetIntrusionGroups`
- **Request body** (`application/json` — `GetIntrusionGroupsRequestContent`)
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`GetIntrusionGroupsResponseContent`)
  - `groups` — array **(required)**
    - _array of_ `string`
  - `everybody` — boolean **(required)**
- Errors: `400`, `403`

### SeeAnalytics

#### `POST` `/v1/permissions/see_analytics/check`

Checks the `can: See analytics` permissions for a specific user for the target.

- operationId: `CheckSeeAnalyticsPermission`
- **Request body** (`application/json` — `CheckSeeAnalyticsPermissionRequestContent`) **(required)**
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `target` — Identity **(required)**
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`CheckSeeAnalyticsPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to use see analytics against the target.
- Errors: `400`, `403`

#### `POST` `/v1/permissions/see_analytics/groups`

Gets a list of groups that are allowed to see the analytics.

- operationId: `GetSeeAnalyticsGroups`
- **Request body** (`application/json` — `GetSeeAnalyticsGroupsRequestContent`)
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`GetSeeAnalyticsGroupsResponseContent`)
  - `groups` — array **(required)**
    - _array of_ `string`
  - `everybody` — boolean **(required)**
- Errors: `400`, `403`

### SeeFullNumber

#### `POST` `/v1/permissions/see_full_number/check`

Checks the `can see: Full number` permissions for a specific user.

- operationId: `CheckCanSeeFullNumberPermission`
- **Request body** (`application/json` — `CheckCanSeeFullNumberPermissionRequestContent`)
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`CheckCanSeeFullNumberPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to see full number the target.
- Errors: `400`, `403`

### SeeTranscriptionSummary

#### `POST` `/v1/permissions/see_transcription_summary/check`

Checks the `can: See transcription summary` permissions for a specific user.

- operationId: `CheckSeeTranscriptionSummaryPermission`
- **Request body** (`application/json` — `CheckSeeTranscriptionSummaryPermissionRequestContent`)
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- **Response 200** (`CheckSeeTranscriptionSummaryPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to see transcription summary.
- Errors: `400`, `403`

### UseAnalytics

#### `POST` `/v1/permissions/use_analytics/check`

Checks the `can use: Analytics` permissions for a specific user for the target.

- operationId: `CheckCanUseAnalyticsPermission`
- **Request body** (`application/json` — `CheckCanUseAnalyticsPermissionRequestContent`)
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`CheckCanUseAnalyticsPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to use analytics the target.
- Errors: `400`, `403`

### Calls

#### `POST` `/v1/permissions/view_calls_of_users/check`

Checks the `can: View calls of users` permissions for a specific user for the list of targets.

- operationId: `CheckCanViewCallsOfUsersPermission`
- **Request body** (`application/json` — `CheckCanViewCallsOfUsersPermissionRequestContent`) **(required)**
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `target` — array **(required)** — A list of users or groups to check whether action is allowed to perform.
    - _array of_ `Identity`
      - `extension` — string
      - `email` — string
      - `userId` — string
      - `groupId` — string
- **Response 200** (`CheckCanViewCallsOfUsersPermissionResponseContent`)
  - `allowed` — boolean **(required)** — True if permitted to view calls against the target.
- Errors: `400`, `403`

#### `POST` `/v1/permissions/view_calls_of_users/groups`

Gets a list of groups that are allowed to view calls of users.

- operationId: `GetViewCallsOfUsersGroups`
- **Request body** (`application/json` — `GetViewCallsOfUsersGroupsRequestContent`)
  - `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
  - `identity` — Identity
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string
- **Response 200** (`GetViewCallsOfUsersGroupsResponseContent`)
  - `groups` — array **(required)**
    - _array of_ `string`
  - `everybody` — boolean **(required)**
- Errors: `400`, `403`

### Schemas appendix — Cloud PBX API (Permissions)

<details><summary>29 component schemas</summary>

**`CheckCanSeeFullNumberPermissionRequestContent`**

- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`CheckCanSeeFullNumberPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to see full number the target.

**`CheckCanUseAnalyticsPermissionRequestContent`**

- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`CheckCanUseAnalyticsPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to use analytics the target.

**`CheckCanViewCallsOfUsersPermissionRequestContent`**

- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string
- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `target` — array **(required)** — A list of users or groups to check whether action is allowed to perform.
  - _array of_ `Identity`
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string

**`CheckCanViewCallsOfUsersPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to view calls against the target.

**`CheckDeleteCallRecordingsOfUsersPermissionRequestContent`**

- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string
- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `target` — array **(required)** — The participants of the call (all flows) or conference. Allowed when at least one of them is in an allowed group.
  - _array of_ `Identity`
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string

**`CheckDeleteCallRecordingsOfUsersPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to delete call recordings, transcriptions and insights of the target.

**`CheckIntrusionPermissionRequestContent`**

- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string
- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `target` — Identity **(required)**
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`CheckIntrusionPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to use instrusion against the target.

**`CheckSeeAnalyticsPermissionRequestContent`**

- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string
- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `target` — Identity **(required)**
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`CheckSeeAnalyticsPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to use see analytics against the target.

**`CheckSeeCallRecordingsPermissionRequestContent`**

- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string
- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.

**`CheckSeeCallRecordingsPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to see call recordings.

**`CheckSeeTranscriptionSummaryPermissionRequestContent`**

- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string
- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.

**`CheckSeeTranscriptionSummaryPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to see transcription summary.

**`CheckViewCallRecordingsOfUsersPermissionRequestContent`**

- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string
- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `target` — array **(required)** — A list of users or groups to check whether action is allowed to perform.
  - _array of_ `Identity`
    - `extension` — string
    - `email` — string
    - `userId` — string
    - `groupId` — string

**`CheckViewCallRecordingsOfUsersPermissionResponseContent`**

- `allowed` — boolean **(required)** — True if permitted to view call recordings against the target.

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetIntrusionGroupsRequestContent`**

- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`GetIntrusionGroupsResponseContent`**

- `groups` — array **(required)**
  - _array of_ `string`
- `everybody` — boolean **(required)**

**`GetSeeAnalyticsGroupsRequestContent`**

- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`GetSeeAnalyticsGroupsResponseContent`**

- `groups` — array **(required)**
  - _array of_ `string`
- `everybody` — boolean **(required)**

**`GetViewCallRecordingsOfUsersGroupsRequestContent`**

- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`GetViewCallRecordingsOfUsersGroupsResponseContent`**

- `groups` — array **(required)**
  - _array of_ `string`
- `everybody` — boolean **(required)**

**`GetViewCallsOfUsersGroupsRequestContent`**

- `domain` — string — A domain of the PBX if service authorization used. This option is ignored for user based authorization.
- `identity` — Identity
  - `extension` — string
  - `email` — string
  - `userId` — string
  - `groupId` — string

**`GetViewCallsOfUsersGroupsResponseContent`**

- `groups` — array **(required)**
  - _array of_ `string`
- `everybody` — boolean **(required)**

**`Identity`**

- `extension` — string
- `email` — string
- `userId` — string
- `groupId` — string

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

</details>
