## Calendar API

_OpenAPI: WIM calendar service — version —_

**Servers**

- `https://wim.wildix.com` — Production
- `https://wim-stable.wildix.com` — Stable
- `https://wim-stage.wildix.com` — Stage

### Other

#### `GET` `/calendar/availability`

- operationId: `CheckAvailability`
- **Parameters**
  - `company` (query) — string **(required)**
  - `email` (query) — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- **Response 200** (`CheckAvailabilityResponseContent`)
  - `success` — boolean
  - `result` — boolean
- Errors: `400`

#### `POST` `/calendar/cancel`

- operationId: `CancelEvent`
- **Request body** (`application/json` — `CancelEventRequestContent`) **(required)**
  - `ownerId` — string **(required)** _(minLen=1)_
  - `eventId` — string **(required)** _(minLen=1)_
  - `emailNotification` — EventNotification
    - `enabled` — boolean — If true, will send email notification to attendees, by default, email notification is sent.
  - `reason` — string
- **Response 200** (`CancelEventResponseContent`)
  - `success` — boolean **(required)**
  - `result` — CancelEventOutputResult **(required)**
    - `event` — CalendarEvent
      - `id` — string **(required)**
      - `calendarId` — string **(required)**
      - `summary` — string **(required)**
      - `description` — string
      - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
      - `attendees` — array **(required)**
        - _array of_ `CalendarEventAttendee`
          - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `name` — string
          - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
      - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
      - `resource` — string **(required)**
      - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
      - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_
- Errors: `400`

#### `GET` `/calendar/events`

Get events active for the resource

- operationId: `ListResourceEvents`
- **Parameters**
  - `resource` (query) — string **(required)** — Used to identify the source of the event. Combination of service(for example 'voicebot') and client identifier(phone number, email or stream id). example: voicebot#1234567890
  - `company` (query) — string **(required)**
  - `email` (query) — string **(required)** — Email of the user who is the owner(agent) of the events. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- **Response 200** (`ListResourceEventsResponseContent`)
  - `items` — array **(required)**
    - _array of_ `CalendarEvent`
      - `id` — string **(required)**
      - `calendarId` — string **(required)**
      - `summary` — string **(required)**
      - `description` — string
      - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
      - `attendees` — array **(required)**
        - _array of_ `CalendarEventAttendee`
          - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `name` — string
          - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
      - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
      - `resource` — string **(required)**
      - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
      - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_
- Errors: `400`, `404`

#### `POST` `/calendar/reschedule`

- operationId: `RescheduleEvent`
- **Request body** (`application/json` — `RescheduleEventRequestContent`) **(required)**
  - `eventId` — string **(required)** _(minLen=1)_
  - `ownerId` — string **(required)** _(minLen=1)_
  - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `duration` — string **(required)** _(minLen=15; maxLen=360)_
  - `reason` — string
  - `summary` — string — Event title _(maxLen=255)_
  - `attendees` — array
    - _array of_ `CalendarEventParticipant`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `name` — string
      - `picture` — string
  - `changed` — array
    - _array of_ `string`
  - `emailNotification` — EventNotification
    - `enabled` — boolean — If true, will send email notification to attendees, by default, email notification is sent.
  - `description` — string — Event description. If not provided, will be generated automatically using default template.
- **Response 200** (`RescheduleEventResponseContent`)
  - `success` — boolean **(required)**
  - `result` — RescheduleEventOutputResult **(required)**
    - `event` — CalendarEvent
      - `id` — string **(required)**
      - `calendarId` — string **(required)**
      - `summary` — string **(required)**
      - `description` — string
      - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
      - `attendees` — array **(required)**
        - _array of_ `CalendarEventAttendee`
          - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `name` — string
          - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
      - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
      - `resource` — string **(required)**
      - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
      - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_
- Errors: `400`, `404`, `500`

#### `POST` `/calendar/schedule`

- operationId: `ScheduleEvent`
- **Request body** (`application/json` — `ScheduleEventRequestContent`) **(required)**
  - `company` — string **(required)**
  - `owner` — CalendarEventParticipant **(required)**
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `name` — string
    - `picture` — string
  - `attendees` — array
    - _array of_ `CalendarEventParticipant`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `name` — string
      - `picture` — string
  - `invitee` — CalendarEventParticipant
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `name` — string
    - `picture` — string
  - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `duration` — string **(required)** _(minLen=15; maxLen=360)_
  - `summary` — string — Event title _(maxLen=255)_
  - `description` — string — Event description. If not provided, will be generated automatically using default template.
  - `resource` — string — Used to identify the source of the event. Combination of service(for example 'voicebot') and client identifier(phone number, email or stream id). example: voicebot#1234567890
  - `emailNotification` — EventNotification
    - `enabled` — boolean — If true, will send email notification to attendees, by default, email notification is sent.
  - `extra` — CalendarEventExtraData
    - `timeZone` — string
- **Response 200** (`ScheduleEventResponseContent`)
  - `success` — boolean
  - `result` — ScheduleEventOutputResult
    - `event` — CalendarEvent
      - `id` — string **(required)**
      - `calendarId` — string **(required)**
      - `summary` — string **(required)**
      - `description` — string
      - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
      - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
      - `attendees` — array **(required)**
        - _array of_ `CalendarEventAttendee`
          - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
          - `name` — string
          - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
      - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
      - `resource` — string **(required)**
      - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
      - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_
- Errors: `400`, `500`

#### `GET` `/calendar/slots`

- operationId: `GetSlots`
- **Parameters**
  - `company` (query) — string **(required)**
  - `email` (query) — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `from` (query) — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])$)_
  - `till` (query) — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])$)_
  - `duration` (query) — string _(minLen=15; maxLen=360)_
  - `timeZone` (query) — string **(required)**
  - `excluded` (query) — string
- **Response 200** (`GetSlotsResponseContent`)
  - `success` — boolean
  - `result` — CalendarAvailability
    - `days` — array
      - _array of_ `CalendarDaySlots`
        - `date` — string
        - `slots` — array
          - _array of_ `CalendarSlot`
            - `startTime` — string
    - `duration` — string _(minLen=15; maxLen=360)_
    - `timeZone` — string
    - `settings` — CalendarAvailabilitySettings
      - `duration` — array
        - _array of_ `string`
- Errors: `400`, `404`

### Schemas appendix — Calendar API

<details><summary>29 component schemas</summary>

**`BadRequestNotFoundErrorResponseContent`**

- `message` — string **(required)**

**`BadRequestValidationErrorResponseContent`**

- `message` — string **(required)**

**`CalendarAvailability`**

- `days` — array
  - _array of_ `CalendarDaySlots`
    - `date` — string
    - `slots` — array
      - _array of_ `CalendarSlot`
        - _(nesting depth limit — see `CalendarSlot` in the Schemas appendix)_
- `duration` — string _(minLen=15; maxLen=360)_
- `timeZone` — string
- `settings` — CalendarAvailabilitySettings
  - `duration` — array
    - _array of_ `string`

**`CalendarAvailabilitySettings`**

- `duration` — array
  - _array of_ `string`

**`CalendarDaySlots`**

- `date` — string
- `slots` — array
  - _array of_ `CalendarSlot`
    - `startTime` — string

**`CalendarEvent`**

- `id` — string **(required)**
- `calendarId` — string **(required)**
- `summary` — string **(required)**
- `description` — string
- `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
- `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
- `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
- `attendees` — array **(required)**
  - _array of_ `CalendarEventAttendee`
    - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `name` — string
    - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
- `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
- `resource` — string **(required)**
- `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
- `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

**`CalendarEventAttendee`**

- `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `name` — string
- `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`CalendarEventAttendeeStatus`**

- string _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`CalendarEventExtraData`**

- `timeZone` — string

**`CalendarEventParticipant`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `name` — string
- `picture` — string

**`CalendarEventStatus`**

- string _(enum: `confirmed`, `tentative`, `cancelled`)_

**`CalendarEventTransparency`**

- string _(enum: `opaque`, `transparent`)_

**`CalendarEventType`**

- string _(enum: `default`, `outOfOffice`)_

**`CalendarEventVisibility`**

- string _(enum: `public`, `private`, `confidential`)_

**`CalendarSlot`**

- `startTime` — string

**`CancelEventOutputResult`**

- `event` — CalendarEvent
  - `id` — string **(required)**
  - `calendarId` — string **(required)**
  - `summary` — string **(required)**
  - `description` — string
  - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
  - `attendees` — array **(required)**
    - _array of_ `CalendarEventAttendee`
      - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `name` — string
      - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
  - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
  - `resource` — string **(required)**
  - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
  - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

**`CancelEventRequestContent`**

- `ownerId` — string **(required)** _(minLen=1)_
- `eventId` — string **(required)** _(minLen=1)_
- `emailNotification` — EventNotification
  - `enabled` — boolean — If true, will send email notification to attendees, by default, email notification is sent.
- `reason` — string

**`CancelEventResponseContent`**

- `success` — boolean **(required)**
- `result` — CancelEventOutputResult **(required)**
  - `event` — CalendarEvent
    - `id` — string **(required)**
    - `calendarId` — string **(required)**
    - `summary` — string **(required)**
    - `description` — string
    - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
    - `attendees` — array **(required)**
      - _array of_ `CalendarEventAttendee`
        - _(nesting depth limit — see `CalendarEventAttendee` in the Schemas appendix)_
    - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
    - `resource` — string **(required)**
    - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
    - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

**`CheckAvailabilityResponseContent`**

- `success` — boolean
- `result` — boolean

**`EventNotification`**

- `enabled` — boolean — If true, will send email notification to attendees, by default, email notification is sent.

**`GetSlotsResponseContent`**

- `success` — boolean
- `result` — CalendarAvailability
  - `days` — array
    - _array of_ `CalendarDaySlots`
      - `date` — string
      - `slots` — array
        - _(nesting depth limit — see `CalendarSlot` in the Schemas appendix)_
  - `duration` — string _(minLen=15; maxLen=360)_
  - `timeZone` — string
  - `settings` — CalendarAvailabilitySettings
    - `duration` — array
      - _array of_ `string`

**`InternalServerErrorResponseContent`**

- `message` — string **(required)**

**`ListResourceEventsResponseContent`**

- `items` — array **(required)**
  - _array of_ `CalendarEvent`
    - `id` — string **(required)**
    - `calendarId` — string **(required)**
    - `summary` — string **(required)**
    - `description` — string
    - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
    - `attendees` — array **(required)**
      - _array of_ `CalendarEventAttendee`
        - _(nesting depth limit — see `CalendarEventAttendee` in the Schemas appendix)_
    - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
    - `resource` — string **(required)**
    - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
    - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

**`RescheduleEventOutputResult`**

- `event` — CalendarEvent
  - `id` — string **(required)**
  - `calendarId` — string **(required)**
  - `summary` — string **(required)**
  - `description` — string
  - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
  - `attendees` — array **(required)**
    - _array of_ `CalendarEventAttendee`
      - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `name` — string
      - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
  - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
  - `resource` — string **(required)**
  - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
  - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

**`RescheduleEventRequestContent`**

- `eventId` — string **(required)** _(minLen=1)_
- `ownerId` — string **(required)** _(minLen=1)_
- `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
- `duration` — string **(required)** _(minLen=15; maxLen=360)_
- `reason` — string
- `summary` — string — Event title _(maxLen=255)_
- `attendees` — array
  - _array of_ `CalendarEventParticipant`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `name` — string
    - `picture` — string
- `changed` — array
  - _array of_ `string`
- `emailNotification` — EventNotification
  - `enabled` — boolean — If true, will send email notification to attendees, by default, email notification is sent.
- `description` — string — Event description. If not provided, will be generated automatically using default template.

**`RescheduleEventResponseContent`**

- `success` — boolean **(required)**
- `result` — RescheduleEventOutputResult **(required)**
  - `event` — CalendarEvent
    - `id` — string **(required)**
    - `calendarId` — string **(required)**
    - `summary` — string **(required)**
    - `description` — string
    - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
    - `attendees` — array **(required)**
      - _array of_ `CalendarEventAttendee`
        - _(nesting depth limit — see `CalendarEventAttendee` in the Schemas appendix)_
    - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
    - `resource` — string **(required)**
    - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
    - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

**`ScheduleEventOutputResult`**

- `event` — CalendarEvent
  - `id` — string **(required)**
  - `calendarId` — string **(required)**
  - `summary` — string **(required)**
  - `description` — string
  - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
  - `attendees` — array **(required)**
    - _array of_ `CalendarEventAttendee`
      - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `name` — string
      - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
  - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
  - `resource` — string **(required)**
  - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
  - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

**`ScheduleEventRequestContent`**

- `company` — string **(required)**
- `owner` — CalendarEventParticipant **(required)**
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `name` — string
  - `picture` — string
- `attendees` — array
  - _array of_ `CalendarEventParticipant`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `name` — string
    - `picture` — string
- `invitee` — CalendarEventParticipant
  - `id` — string **(required)** _(minLen=12; maxLen=12)_
  - `email` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `name` — string
  - `picture` — string
- `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
- `duration` — string **(required)** _(minLen=15; maxLen=360)_
- `summary` — string — Event title _(maxLen=255)_
- `description` — string — Event description. If not provided, will be generated automatically using default template.
- `resource` — string — Used to identify the source of the event. Combination of service(for example 'voicebot') and client identifier(phone number, email or stream id). example: voicebot#1234567890
- `emailNotification` — EventNotification
  - `enabled` — boolean — If true, will send email notification to attendees, by default, email notification is sent.
- `extra` — CalendarEventExtraData
  - `timeZone` — string

**`ScheduleEventResponseContent`**

- `success` — boolean
- `result` — ScheduleEventOutputResult
  - `event` — CalendarEvent
    - `id` — string **(required)**
    - `calendarId` — string **(required)**
    - `summary` — string **(required)**
    - `description` — string
    - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `end` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
    - `owner` — string **(required)** _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `status` — string **(required)** _(enum: `confirmed`, `tentative`, `cancelled`)_
    - `attendees` — array **(required)**
      - _array of_ `CalendarEventAttendee`
        - _(nesting depth limit — see `CalendarEventAttendee` in the Schemas appendix)_
    - `type` — string **(required)** _(enum: `default`, `outOfOffice`)_
    - `resource` — string **(required)**
    - `transparency` — string **(required)** _(enum: `opaque`, `transparent`)_
    - `visibility` — string **(required)** _(enum: `public`, `private`, `confidential`)_

</details>
