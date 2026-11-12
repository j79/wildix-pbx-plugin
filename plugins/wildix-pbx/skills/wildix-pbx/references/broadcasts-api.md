## Broadcasts API (x-hoppers)

_OpenAPI: Broadcast API is an event management mechanism where each action serves as a trigger for executing business logic and broadcasting data. — version v1_

**Servers**

- `https://broadcasts.x-hoppers.com` — Production
- `https://broadcasts-stable.x-hoppers.com` — Stable
- `https://broadcasts-stage.x-hoppers.com` — Stage

### Other

#### `GET` `/v1/broadcasts`

- operationId: `ListBroadcasts`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListBroadcastsResponseContent`)
  - `broadcasts` — array **(required)**
    - _array of_ `Broadcast`
      - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
      - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
        - _array of_ `string`
      - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
      - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/broadcasts`

- operationId: `CreateBroadcast`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateBroadcastRequestContent`) **(required)**
  - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
  - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
    - _array of_ `string`
  - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
  - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- **Response 201** (`CreateBroadcastResponseContent`)
  - `broadcast` — Broadcast **(required)**
    - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
    - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
      - _array of_ `string`
    - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
    - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/broadcasts-messages/schedules`

- operationId: `ListSchedules`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListSchedulesResponseContent`)
  - `schedules` — array
    - _array of_ `Schedule`
      - `companyId` — string _(minLen=3; maxLen=30)_
      - `timezone` — string **(required)** — Timezone in IANA format
      - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
        - _array of_ `string`
      - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
        - _array of_ `string`
      - `message` — string **(required)** _(minLen=3; maxLen=1000)_
      - `schedule` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`once`**
            - `once` — OnceScheduleConfig **(required)**
              - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
              - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - **`daily`**
            - `daily` — DailyScheduleConfig **(required)**
              - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - **`weekly`**
            - `weekly` — WeeklyScheduleConfig **(required)**
              - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
              - `days` — array **(required)**
                - _array of_ `number`
          - **`monthly`**
            - `monthly` — MonthlyScheduleConfig **(required)**
              - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
              - `days` — array **(required)**
                - _array of_ `number`
          - **`yearly`**
            - `yearly` — YearlyScheduleConfig **(required)**
              - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
              - `days` — array **(required)**
                - _array of_ `number`
              - `months` — array **(required)**
                - _array of_ `number`
      - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
      - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
      - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
      - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
        - _array of_ `string`
      - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `isActive` — boolean **(required)** _(default=True)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/broadcasts-messages/schedules`

- operationId: `CreateSchedule`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateScheduleRequestContent`) **(required)**
  - `timezone` — string **(required)** — Timezone in IANA format
  - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
    - _array of_ `string`
  - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
    - _array of_ `string`
  - `message` — string **(required)** _(minLen=3; maxLen=1000)_
  - `schedule` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`once`**
        - `once` — OnceScheduleConfig **(required)**
          - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
      - **`daily`**
        - `daily` — DailyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
      - **`weekly`**
        - `weekly` — WeeklyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - `days` — array **(required)**
            - _array of_ `number`
      - **`monthly`**
        - `monthly` — MonthlyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - `days` — array **(required)**
            - _array of_ `number`
      - **`yearly`**
        - `yearly` — YearlyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - `days` — array **(required)**
            - _array of_ `number`
          - `months` — array **(required)**
            - _array of_ `number`
  - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
  - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
  - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
    - _array of_ `string`
  - `isActive` — boolean **(required)** _(default=True)_
- **Response 201** (`CreateScheduleResponseContent`)
  - `schedule` — Schedule **(required)**
    - `companyId` — string _(minLen=3; maxLen=30)_
    - `timezone` — string **(required)** — Timezone in IANA format
    - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
      - _array of_ `string`
    - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
      - _array of_ `string`
    - `message` — string **(required)** _(minLen=3; maxLen=1000)_
    - `schedule` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`once`**
          - `once` — OnceScheduleConfig **(required)**
            - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - **`daily`**
          - `daily` — DailyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - **`weekly`**
          - `weekly` — WeeklyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
        - **`monthly`**
          - `monthly` — MonthlyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
        - **`yearly`**
          - `yearly` — YearlyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
            - `months` — array **(required)**
              - _array of_ `number`
    - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
    - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
    - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `isActive` — boolean **(required)** _(default=True)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/broadcasts-messages/schedules/{id}`

- operationId: `GetSchedule`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetScheduleResponseContent`)
  - `schedule` — Schedule **(required)**
    - `companyId` — string _(minLen=3; maxLen=30)_
    - `timezone` — string **(required)** — Timezone in IANA format
    - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
      - _array of_ `string`
    - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
      - _array of_ `string`
    - `message` — string **(required)** _(minLen=3; maxLen=1000)_
    - `schedule` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`once`**
          - `once` — OnceScheduleConfig **(required)**
            - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - **`daily`**
          - `daily` — DailyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - **`weekly`**
          - `weekly` — WeeklyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
        - **`monthly`**
          - `monthly` — MonthlyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
        - **`yearly`**
          - `yearly` — YearlyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
            - `months` — array **(required)**
              - _array of_ `number`
    - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
    - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
    - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `isActive` — boolean **(required)** _(default=True)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `PUT` `/v1/broadcasts-messages/schedules/{id}`

- operationId: `UpdateSchedule`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateScheduleRequestContent`) **(required)**
  - `timezone` — string **(required)** — Timezone in IANA format
  - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
    - _array of_ `string`
  - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
    - _array of_ `string`
  - `message` — string **(required)** _(minLen=3; maxLen=1000)_
  - `schedule` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`once`**
        - `once` — OnceScheduleConfig **(required)**
          - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
      - **`daily`**
        - `daily` — DailyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
      - **`weekly`**
        - `weekly` — WeeklyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - `days` — array **(required)**
            - _array of_ `number`
      - **`monthly`**
        - `monthly` — MonthlyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - `days` — array **(required)**
            - _array of_ `number`
      - **`yearly`**
        - `yearly` — YearlyScheduleConfig **(required)**
          - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
          - `days` — array **(required)**
            - _array of_ `number`
          - `months` — array **(required)**
            - _array of_ `number`
  - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
  - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
  - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
    - _array of_ `string`
  - `isActive` — boolean
- **Response 200** (`UpdateScheduleResponseContent`)
  - `schedule` — Schedule **(required)**
    - `companyId` — string _(minLen=3; maxLen=30)_
    - `timezone` — string **(required)** — Timezone in IANA format
    - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
      - _array of_ `string`
    - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
      - _array of_ `string`
    - `message` — string **(required)** _(minLen=3; maxLen=1000)_
    - `schedule` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`once`**
          - `once` — OnceScheduleConfig **(required)**
            - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - **`daily`**
          - `daily` — DailyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - **`weekly`**
          - `weekly` — WeeklyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
        - **`monthly`**
          - `monthly` — MonthlyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
        - **`yearly`**
          - `yearly` — YearlyScheduleConfig **(required)**
            - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
            - `days` — array **(required)**
              - _array of_ `number`
            - `months` — array **(required)**
              - _array of_ `number`
    - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
    - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
    - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `isActive` — boolean **(required)** _(default=True)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `DELETE` `/v1/broadcasts-messages/schedules/{id}`

- operationId: `DeleteSchedule`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/broadcasts-messages/send`

Sends a message to specific broadcasts.

- operationId: `SendMessage`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `SendMessageRequestContent`) **(required)**
  - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
    - _array of_ `string`
  - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
    - _array of_ `string`
  - `message` — string **(required)** — Message for sending to specific broadcasts. _(minLen=3; maxLen=1000)_
  - `mode` — string _(enum: `default`, `voice`)_
  - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
  - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
  - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
    - _array of_ `string`
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/broadcasts/{broadcastId}`

- operationId: `GetBroadcast`
- **Parameters**
  - `broadcastId` (path) — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetBroadcastResponseContent`)
  - `broadcast` — Broadcast **(required)**
    - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
    - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
      - _array of_ `string`
    - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
    - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `PUT` `/v1/broadcasts/{broadcastId}`

- operationId: `UpdateBroadcast`
- **Parameters**
  - `broadcastId` (path) — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateBroadcastRequestContent`) **(required)**
  - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
  - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
    - _array of_ `string`
  - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
  - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
- **Response 200** (`UpdateBroadcastResponseContent`)
  - `broadcast` — Broadcast **(required)**
    - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
    - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
      - _array of_ `string`
    - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
    - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `DELETE` `/v1/broadcasts/{broadcastId}`

- operationId: `DeleteBroadcast`
- **Parameters**
  - `broadcastId` (path) — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/broadcasts/{broadcastId}/files`

Creates a file that can be broadcasted within the chat associated with a broadcast.
After the file object is created, the file content must be uploaded to the provided `presignedUploadUrl`.
The correct `Content-Type` header should be specified during the upload process.

- operationId: `BroadcastFile`
- **Parameters**
  - `broadcastId` (path) — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `BroadcastFileRequestContent`) **(required)**
  - `name` — string **(required)** — The name of the file. Unreadable characters will be replaced with underscores. _(minLen=1; maxLen=255)_
- **Response 200** (`BroadcastFileResponseContent`)
  - `fileId` — string **(required)** — The unique identifier of the file.
  - `presignedUploadUrl` — string **(required)** — The presigned URL for uploading the file.
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/broadcasts/{broadcastId}/transcriptions`

Shares the transcription of an audio message within the chat associated with a broadcast.
The message can be sent on behalf of a specified user. If the `user` is set to system, the message will be sent on behalf of the `bot`.

- operationId: `BroadcastTranscription`
- **Parameters**
  - `broadcastId` (path) — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `BroadcastTranscriptionRequestContent`) **(required)**
  - `owner` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`system`**
        - `system` — boolean **(required)**
      - **`user`**
        - `user` — BroadcastTriggerUser **(required)**
          - `email` — string **(required)**
  - `audioTranscription` — string **(required)** _(minLen=1; maxLen=4000)_
  - `audioFileId` — string
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/quick-response-templates`

- operationId: `ListQuickResponseTemplates`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListQuickResponseTemplatesResponseContent`)
  - `templates` — array **(required)**
    - _array of_ `QuickResponseTemplate`
      - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
      - `type` — string **(required)** _(enum: `shelf`, `a4`)_
      - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
      - `description` — string _(maxLen=1000)_
      - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
      - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
      - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
      - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/quick-response-templates`

- operationId: `CreateQuickResponseTemplate`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateQuickResponseTemplateRequestContent`) **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `type` — string **(required)** _(enum: `shelf`, `a4`)_
  - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `description` — string _(maxLen=1000)_
  - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
  - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
- **Response 201** (`CreateQuickResponseTemplateResponseContent`)
  - `template` — QuickResponseTemplate **(required)**
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `type` — string **(required)** _(enum: `shelf`, `a4`)_
    - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `description` — string _(maxLen=1000)_
    - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
    - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/quick-response-templates/{templateId}`

- operationId: `GetQuickResponseTemplate`
- **Parameters**
  - `templateId` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetQuickResponseTemplateResponseContent`)
  - `template` — QuickResponseTemplate **(required)**
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `type` — string **(required)** _(enum: `shelf`, `a4`)_
    - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `description` — string _(maxLen=1000)_
    - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
    - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `PUT` `/v1/quick-response-templates/{templateId}`

- operationId: `UpdateQuickResponseTemplate`
- **Parameters**
  - `templateId` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateQuickResponseTemplateRequestContent`) **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `type` — string **(required)** _(enum: `shelf`, `a4`)_
  - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `description` — string _(maxLen=1000)_
  - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
  - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
- **Response 200** (`UpdateQuickResponseTemplateResponseContent`)
  - `template` — QuickResponseTemplate **(required)**
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `type` — string **(required)** _(enum: `shelf`, `a4`)_
    - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `description` — string _(maxLen=1000)_
    - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
    - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `DELETE` `/v1/quick-response-templates/{templateId}`

- operationId: `DeleteQuickResponseTemplate`
- **Parameters**
  - `templateId` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/quick-responses`

- operationId: `ListQuickResponses`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `exclusiveStartKey` (query) — string — The key used to start listing from a specific point, for pagination purposes.
- **Response 200** (`ListQuickResponsesResponseContent`)
  - `qrs` — array **(required)**
    - _array of_ `QuickResponse`
      - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
      - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
      - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
      - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
      - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
      - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
      - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
      - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
      - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
      - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
        - _array of_ `string`
      - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
  - `lastEvaluatedKey` — string — The key used for pagination to fetch the next set of results. This field is absent if there are no more results.
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/quick-responses`

- operationId: `CreateQuickResponse`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `CreateQuickResponseRequestContent`) **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
  - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
  - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
  - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
  - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
  - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
    - _array of_ `string`
- **Response 201** (`CreateQuickResponseResponseContent`)
  - `qr` — QuickResponse **(required)**
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
    - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
    - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
    - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
    - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
    - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `GET` `/v1/quick-responses/{id}`

- operationId: `GetQuickResponse`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetQuickResponseResponseContent`)
  - `qr` — QuickResponse **(required)**
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
    - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
    - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
    - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
    - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
    - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `PUT` `/v1/quick-responses/{id}`

- operationId: `UpdateQuickResponse`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Request body** (`application/json` — `UpdateQuickResponseRequestContent`) **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
  - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
  - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
  - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
  - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
  - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
    - _array of_ `string`
- **Response 200** (`UpdateQuickResponseResponseContent`)
  - `qr` — QuickResponse **(required)**
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
    - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
    - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
    - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
    - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
    - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `500`

#### `DELETE` `/v1/quick-responses/{id}`

- operationId: `DeleteQuickResponse`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- Errors: `400`, `403`, `404`, `500`

#### `POST` `/v1/quick-responses/{id}/trigger`

Trigger a Quick Response by its ID.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| ANY | 60 | 10 |
| ANY | 3600 | 100 |

- operationId: `TriggerQuickResponse`
- **Parameters**
  - `id` (path) — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- **Request body** (`application/json` — `TriggerQuickResponseRequestContent`)
  - `parameters` — QuickResponseParametersMap
    - _map of_ `string`
- **Response 200** (`TriggerQuickResponseResponseContent`)
  - `result` — QuickResponseTriggerResult **(required)**
    - `message` — string **(required)** — Result message after successful action execution
    - `redirectUrl` — string — Url for redirecting to another page after execution
- Errors: `400`, `403`, `404`, `429`, `500`

#### `GET` `/v1/skills`

Returns the list of unique skill names (LDAP department names) of the company's PBX. Used to populate the skills filter in broadcast forms.

- operationId: `GetSkills`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`GetSkillsResponseContent`)
  - `skills` — array **(required)** _(maxItems=50)_
    - _array of_ `string`
- Errors: `400`, `403`, `404`, `500`

### Schemas appendix — Broadcasts API (x-hoppers)

<details><summary>54 component schemas</summary>

**`Broadcast`**

- `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
- `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
  - _array of_ `string`
- `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
- `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`BroadcastFileRequestContent`**

- `name` — string **(required)** — The name of the file. Unreadable characters will be replaced with underscores. _(minLen=1; maxLen=255)_

**`BroadcastFileResponseContent`**

- `fileId` — string **(required)** — The unique identifier of the file.
- `presignedUploadUrl` — string **(required)** — The presigned URL for uploading the file.

**`BroadcastTranscriptionRequestContent`**

- `owner` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`system`**
      - `system` — boolean **(required)**
    - **`user`**
      - `user` — BroadcastTriggerUser **(required)**
        - `email` — string **(required)**
- `audioTranscription` — string **(required)** _(minLen=1; maxLen=4000)_
- `audioFileId` — string

**`BroadcastTriggerOwner`**

- _oneOf_ — exactly one of:
  - **`system`**
    - `system` — boolean **(required)**
  - **`user`**
    - `user` — BroadcastTriggerUser **(required)**
      - `email` — string **(required)**

**`BroadcastTriggerUser`**

- `email` — string **(required)**

**`CreateBroadcastRequestContent`**

- `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
- `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
  - _array of_ `string`
- `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
- `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`CreateBroadcastResponseContent`**

- `broadcast` — Broadcast **(required)**
  - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
  - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
    - _array of_ `string`
  - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
  - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`CreateQuickResponseRequestContent`**

- `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
- `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
- `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
- `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
- `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
- `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
- `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
- `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
- `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
- `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
  - _array of_ `string`

**`CreateQuickResponseResponseContent`**

- `qr` — QuickResponse **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
  - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
  - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
  - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
  - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
  - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
    - _array of_ `string`
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`CreateQuickResponseTemplateRequestContent`**

- `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
- `type` — string **(required)** _(enum: `shelf`, `a4`)_
- `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
- `description` — string _(maxLen=1000)_
- `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
- `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
- `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_

**`CreateQuickResponseTemplateResponseContent`**

- `template` — QuickResponseTemplate **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `type` — string **(required)** _(enum: `shelf`, `a4`)_
  - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `description` — string _(maxLen=1000)_
  - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
  - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`CreateScheduleRequestContent`**

- `timezone` — string **(required)** — Timezone in IANA format
- `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
  - _array of_ `string`
- `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
  - _array of_ `string`
- `message` — string **(required)** _(minLen=3; maxLen=1000)_
- `schedule` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`once`**
      - `once` — OnceScheduleConfig **(required)**
        - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
    - **`daily`**
      - `daily` — DailyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
    - **`weekly`**
      - `weekly` — WeeklyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
    - **`monthly`**
      - `monthly` — MonthlyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
    - **`yearly`**
      - `yearly` — YearlyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
        - `months` — array **(required)**
          - _array of_ `number`
- `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
- `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
- `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
- `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
  - _array of_ `string`
- `isActive` — boolean **(required)** _(default=True)_

**`CreateScheduleResponseContent`**

- `schedule` — Schedule **(required)**
  - `companyId` — string _(minLen=3; maxLen=30)_
  - `timezone` — string **(required)** — Timezone in IANA format
  - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
    - _array of_ `string`
  - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
    - _array of_ `string`
  - `message` — string **(required)** _(minLen=3; maxLen=1000)_
  - `schedule` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`once`**
        - `once` — OnceScheduleConfig **(required)**
          - _(nesting depth limit — see `OnceScheduleConfig` in the Schemas appendix)_
      - **`daily`**
        - `daily` — DailyScheduleConfig **(required)**
          - _(nesting depth limit — see `DailyScheduleConfig` in the Schemas appendix)_
      - **`weekly`**
        - `weekly` — WeeklyScheduleConfig **(required)**
          - _(nesting depth limit — see `WeeklyScheduleConfig` in the Schemas appendix)_
      - **`monthly`**
        - `monthly` — MonthlyScheduleConfig **(required)**
          - _(nesting depth limit — see `MonthlyScheduleConfig` in the Schemas appendix)_
      - **`yearly`**
        - `yearly` — YearlyScheduleConfig **(required)**
          - _(nesting depth limit — see `YearlyScheduleConfig` in the Schemas appendix)_
  - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
  - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
  - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
    - _array of_ `string`
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `isActive` — boolean **(required)** _(default=True)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`DailyScheduleConfig`**

- `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetBroadcastResponseContent`**

- `broadcast` — Broadcast **(required)**
  - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
  - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
    - _array of_ `string`
  - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
  - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetQuickResponseResponseContent`**

- `qr` — QuickResponse **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
  - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
  - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
  - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
  - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
  - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
    - _array of_ `string`
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetQuickResponseTemplateResponseContent`**

- `template` — QuickResponseTemplate **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `type` — string **(required)** _(enum: `shelf`, `a4`)_
  - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `description` — string _(maxLen=1000)_
  - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
  - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetScheduleResponseContent`**

- `schedule` — Schedule **(required)**
  - `companyId` — string _(minLen=3; maxLen=30)_
  - `timezone` — string **(required)** — Timezone in IANA format
  - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
    - _array of_ `string`
  - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
    - _array of_ `string`
  - `message` — string **(required)** _(minLen=3; maxLen=1000)_
  - `schedule` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`once`**
        - `once` — OnceScheduleConfig **(required)**
          - _(nesting depth limit — see `OnceScheduleConfig` in the Schemas appendix)_
      - **`daily`**
        - `daily` — DailyScheduleConfig **(required)**
          - _(nesting depth limit — see `DailyScheduleConfig` in the Schemas appendix)_
      - **`weekly`**
        - `weekly` — WeeklyScheduleConfig **(required)**
          - _(nesting depth limit — see `WeeklyScheduleConfig` in the Schemas appendix)_
      - **`monthly`**
        - `monthly` — MonthlyScheduleConfig **(required)**
          - _(nesting depth limit — see `MonthlyScheduleConfig` in the Schemas appendix)_
      - **`yearly`**
        - `yearly` — YearlyScheduleConfig **(required)**
          - _(nesting depth limit — see `YearlyScheduleConfig` in the Schemas appendix)_
  - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
  - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
  - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
    - _array of_ `string`
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `isActive` — boolean **(required)** _(default=True)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetSkillsResponseContent`**

- `skills` — array **(required)** _(maxItems=50)_
  - _array of_ `string`

**`InternalServerErrorResponseContent`**

- `message` — string **(required)**

**`ListBroadcastsResponseContent`**

- `broadcasts` — array **(required)**
  - _array of_ `Broadcast`
    - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
    - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
      - _array of_ `string`
    - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
    - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`ListQuickResponseTemplatesResponseContent`**

- `templates` — array **(required)**
  - _array of_ `QuickResponseTemplate`
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `type` — string **(required)** _(enum: `shelf`, `a4`)_
    - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
    - `description` — string _(maxLen=1000)_
    - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
    - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`ListQuickResponsesResponseContent`**

- `qrs` — array **(required)**
  - _array of_ `QuickResponse`
    - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
    - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
    - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
    - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
    - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
    - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
    - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
    - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- `lastEvaluatedKey` — string — The key used for pagination to fetch the next set of results. This field is absent if there are no more results.

**`ListSchedulesResponseContent`**

- `schedules` — array
  - _array of_ `Schedule`
    - `companyId` — string _(minLen=3; maxLen=30)_
    - `timezone` — string **(required)** — Timezone in IANA format
    - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
      - _array of_ `string`
    - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
      - _array of_ `string`
    - `message` — string **(required)** _(minLen=3; maxLen=1000)_
    - `schedule` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`once`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`daily`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`weekly`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`monthly`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`yearly`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
    - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
    - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
    - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
      - _array of_ `string`
    - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
    - `isActive` — boolean **(required)** _(default=True)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`MonthlyScheduleConfig`**

- `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
- `days` — array **(required)**
  - _array of_ `number`

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`OnceScheduleConfig`**

- `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
- `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_

**`QuickResponse`**

- `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
- `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
- `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
- `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
- `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
- `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
- `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
- `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
- `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
- `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
  - _array of_ `string`
- `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`QuickResponseParametersMap`**

- _map of_ `string`

**`QuickResponseTemplate`**

- `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
- `type` — string **(required)** _(enum: `shelf`, `a4`)_
- `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
- `description` — string _(maxLen=1000)_
- `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
- `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
- `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
- `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`QuickResponseTemplateType`**

- string _(enum: `shelf`, `a4`)_

**`QuickResponseTriggerResult`**

- `message` — string **(required)** — Result message after successful action execution
- `redirectUrl` — string — Url for redirecting to another page after execution

**`QuickResponseType`**

- string _(enum: `BROADCAST_MESSAGE`)_

**`RateLimitExceededExceptionResponseContent`**

- `message` — string **(required)** _(default=Too Many Requests)_

**`Schedule`**

- `companyId` — string _(minLen=3; maxLen=30)_
- `timezone` — string **(required)** — Timezone in IANA format
- `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
  - _array of_ `string`
- `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
  - _array of_ `string`
- `message` — string **(required)** _(minLen=3; maxLen=1000)_
- `schedule` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`once`**
      - `once` — OnceScheduleConfig **(required)**
        - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
    - **`daily`**
      - `daily` — DailyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
    - **`weekly`**
      - `weekly` — WeeklyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
    - **`monthly`**
      - `monthly` — MonthlyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
    - **`yearly`**
      - `yearly` — YearlyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
        - `months` — array **(required)**
          - _array of_ `number`
- `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
- `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
- `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
- `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
  - _array of_ `string`
- `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
- `isActive` — boolean **(required)** _(default=True)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`ScheduleConfig`**

- _oneOf_ — exactly one of:
  - **`once`**
    - `once` — OnceScheduleConfig **(required)**
      - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
      - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
  - **`daily`**
    - `daily` — DailyScheduleConfig **(required)**
      - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
  - **`weekly`**
    - `weekly` — WeeklyScheduleConfig **(required)**
      - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
      - `days` — array **(required)**
        - _array of_ `number`
  - **`monthly`**
    - `monthly` — MonthlyScheduleConfig **(required)**
      - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
      - `days` — array **(required)**
        - _array of_ `number`
  - **`yearly`**
    - `yearly` — YearlyScheduleConfig **(required)**
      - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
      - `days` — array **(required)**
        - _array of_ `number`
      - `months` — array **(required)**
        - _array of_ `number`

**`SendMessageModes`**

- string _(enum: `default`, `voice`)_

**`SendMessageRequestContent`**

- `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
  - _array of_ `string`
- `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
  - _array of_ `string`
- `message` — string **(required)** — Message for sending to specific broadcasts. _(minLen=3; maxLen=1000)_
- `mode` — string _(enum: `default`, `voice`)_
- `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
- `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
- `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
- `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
  - _array of_ `string`

**`ServiceValidationError`**

- `path` — string **(required)**
- `reason` — string **(required)**
- `code` — string **(required)**

**`ServiceValidationErrorsResponseContent`**

- `message` — string **(required)** _(default=Validation error)_
- `errors` — array **(required)**
  - _array of_ `ServiceValidationError`
    - `path` — string **(required)**
    - `reason` — string **(required)**
    - `code` — string **(required)**

**`TriggerQuickResponseRequestContent`**

- `parameters` — QuickResponseParametersMap
  - _map of_ `string`

**`TriggerQuickResponseResponseContent`**

- `result` — QuickResponseTriggerResult **(required)**
  - `message` — string **(required)** — Result message after successful action execution
  - `redirectUrl` — string — Url for redirecting to another page after execution

**`UpdateBroadcastRequestContent`**

- `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
- `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
  - _array of_ `string`
- `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
- `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.

**`UpdateBroadcastResponseContent`**

- `broadcast` — Broadcast **(required)**
  - `pbxSerial` — string **(required)** _(minLen=12; maxLen=12)_
  - `tags` — array **(required)** — A list of tags associated with the broadcast. Tags help group and locate broadcasts based on the specified tag. Duplicate tags in the list will be automatically removed. _(maxItems=20)_
    - _array of_ `string`
  - `isTranscribeEnabled` — boolean — Enables transcription of audio messages from the audio conference. If enabled, transcribed messages will be logged in the chat associated with the broadcast.
  - `isDefault` — boolean — Marks the broadcast as the default for a specific installation. If another broadcast with the same `pbxSerial` is already set as default, the system will automatically remove the 'isDefault' flag from the previous broadcast.
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`UpdateQuickResponseRequestContent`**

- `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
- `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
- `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
- `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
- `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
- `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
- `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
- `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
- `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
- `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
  - _array of_ `string`

**`UpdateQuickResponseResponseContent`**

- `qr` — QuickResponse **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `broadcastId` — string **(required)** _(pattern=^[0-9a-z]{12}$; minLen=12; maxLen=12)_
  - `type` — string **(required)** _(enum: `BROADCAST_MESSAGE`)_
  - `broadcastMessage` — string **(required)** — Message for sending in related conversation and text to speech notification in associated conference. _(pattern=^[\p{L}0-9!?., '`\-–\{\}]*$; minLen=3; maxLen=255)_
  - `playFrequency` — number **(required)** — How often (each N seconds) a request has to be repeated. _(min=5; max=30)_
  - `confirmationTimeout` — number **(required)** — How many seconds the request should wait for the confirmation after the start. _(min=0; max=600)_
  - `queueTimeout` — number **(required)** — How many seconds the queued request should wait for starting processing. _(min=5; max=600)_
  - `comfortGreetingMessage` — string — Message to be displayed on the page after scanning quick response code. _(maxLen=255)_
  - `redirectUrl` — string — Url for redirecting to another page after execution _(pattern=^(https?:\/\/([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(:\d+)?(\/[^\s]*)?)?$; maxLen=1000)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within the broadcast. Empty or absent means no filtering — message plays to all subscribers in the broadcast. _(maxItems=50)_
    - _array of_ `string`
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`UpdateQuickResponseTemplateRequestContent`**

- `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
- `type` — string **(required)** _(enum: `shelf`, `a4`)_
- `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
- `description` — string _(maxLen=1000)_
- `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
- `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
- `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_

**`UpdateQuickResponseTemplateResponseContent`**

- `template` — QuickResponseTemplate **(required)**
  - `name` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `type` — string **(required)** _(enum: `shelf`, `a4`)_
  - `title` — string **(required)** _(pattern=^[\p{L}0-9!?., '’\-–\{\}]*$; minLen=3; maxLen=255)_
  - `description` — string _(maxLen=1000)_
  - `logo` — string — Logo image reference (URL or data URI) shown on the printed template. Max length 262144 = 256 * 1024 bytes (256 KiB). _(maxLen=262144)_
  - `backgroundColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `textColor` — string **(required)** _(pattern=^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$)_
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`UpdateScheduleRequestContent`**

- `timezone` — string **(required)** — Timezone in IANA format
- `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
  - _array of_ `string`
- `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
  - _array of_ `string`
- `message` — string **(required)** _(minLen=3; maxLen=1000)_
- `schedule` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`once`**
      - `once` — OnceScheduleConfig **(required)**
        - `date` — string **(required)** — Date in yyyy-mm-dd format _(pattern=^(\d{4})-(\d{2})-(\d{2})$)_
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
    - **`daily`**
      - `daily` — DailyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
    - **`weekly`**
      - `weekly` — WeeklyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
    - **`monthly`**
      - `monthly` — MonthlyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
    - **`yearly`**
      - `yearly` — YearlyScheduleConfig **(required)**
        - `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
        - `days` — array **(required)**
          - _array of_ `number`
        - `months` — array **(required)**
          - _array of_ `number`
- `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
- `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
- `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
- `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
  - _array of_ `string`
- `isActive` — boolean

**`UpdateScheduleResponseContent`**

- `schedule` — Schedule **(required)**
  - `companyId` — string _(minLen=3; maxLen=30)_
  - `timezone` — string **(required)** — Timezone in IANA format
  - `broadcastIds` — array — A list of broadcast's IDs. BroadcastIds or tags list must be provided.
    - _array of_ `string`
  - `tags` — array — A list of tags associated with the broadcasts. BroadcastIds or tags list must be provided. _(maxItems=20)_
    - _array of_ `string`
  - `message` — string **(required)** _(minLen=3; maxLen=1000)_
  - `schedule` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`once`**
        - `once` — OnceScheduleConfig **(required)**
          - _(nesting depth limit — see `OnceScheduleConfig` in the Schemas appendix)_
      - **`daily`**
        - `daily` — DailyScheduleConfig **(required)**
          - _(nesting depth limit — see `DailyScheduleConfig` in the Schemas appendix)_
      - **`weekly`**
        - `weekly` — WeeklyScheduleConfig **(required)**
          - _(nesting depth limit — see `WeeklyScheduleConfig` in the Schemas appendix)_
      - **`monthly`**
        - `monthly` — MonthlyScheduleConfig **(required)**
          - _(nesting depth limit — see `MonthlyScheduleConfig` in the Schemas appendix)_
      - **`yearly`**
        - `yearly` — YearlyScheduleConfig **(required)**
          - _(nesting depth limit — see `YearlyScheduleConfig` in the Schemas appendix)_
  - `playFrequency` — number — The message repeat interval in seconds. _(min=5; max=30)_
  - `confirmationTimeout` — number — The duration in seconds before the response is canceled. _(min=0; max=600)_
  - `queueTimeout` — number — How long the message stays in the queue. _(min=5; max=600)_
  - `skills` — array — A list of skills (LDAP department names) to filter notification recipients within selected broadcasts. Empty or absent means no filtering — message plays to all subscribers in the broadcasts. _(maxItems=50)_
    - _array of_ `string`
  - `id` — string **(required)** _(pattern=^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$; minLen=36; maxLen=36)_
  - `isActive` — boolean **(required)** _(default=True)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`WeeklyScheduleConfig`**

- `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
- `days` — array **(required)**
  - _array of_ `number`

**`YearlyScheduleConfig`**

- `time` — string **(required)** — Time in hh:mm format _(pattern=^(?:[01]\d|2[0-3]):[0-5]\d$)_
- `days` — array **(required)**
  - _array of_ `number`
- `months` — array **(required)**
  - _array of_ `number`

</details>
