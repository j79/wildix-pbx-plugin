## Kite API

_OpenAPI: x-bees kite service — version v2_

**Servers**

- `https://api.x-bees.com` — Production
- `https://api-stable.x-bees.com` — Stable
- `https://api-stage.x-bees.com` — Stage

### Other

#### `POST` `/v2/kite/agents`

Retrieves a list of agents available for Kite-based conversations, filtered by service, extensions, or emails.

- operationId: `ListAgents`
- **Scopes**: `kite:ListAgents`, `kite:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the organization when a service token is used.
- **Request body** (`application/json` — `ListAgentsRequestContent`) **(required)**
  - `filter` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — string **(required)** — The unique identifier of the service which represent URI (example - 2@example.wildixin.com:443).
      - **`extensions`**
        - `extensions` — array **(required)** — A list of extensions that could be used inside Kite based conversation.
          - _array of_ `string`
      - **`emails`**
        - `emails` — array **(required)** — A list of emails that could be used inside Kite based conversation.
          - _array of_ `string`
- **Response 200** (`ListAgentsResponseContent`)
  - `users` — array **(required)**
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
- Errors: `400`, `403`, `404`, `429`

#### `PATCH` `/v2/kite/calendar/channels/{channelId}/events/{eventOwner}/{eventId}`

Reschedules an existing calendar event, updating its time, duration, attendees, or other details.

- operationId: `RescheduleCalendarEvent`
- **Scopes**: `kite:RescheduleCalendarEvent`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or john.doe@example.com). _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `eventId` (path) — string **(required)**
  - `eventOwner` (path) — string **(required)**
- **Request body** (`application/json` — `RescheduleCalendarEventRequestContent`)
  - `start` — string _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `duration` — string _(minLen=15; maxLen=360)_
  - `reason` — string
  - `summary` — string — Event title _(maxLen=255)_
  - `attendees` — array
    - _array of_ `string`
  - `changed` — array
    - _array of_ `string`
- **Response 200** (`RescheduleCalendarEventResponseContent`)
  - `channel` — Channel **(required)**
    - `subject` — string
    - `description` — string
    - `picture` — string — Picture URL
    - `pictureColor` — string — Picture dominant color represented by a hex value.
    - `access` — string _(enum: `private`, `public`)_
    - `company` — string
    - `context` — ChannelContext
      - `source` — string _(enum: `kite`)_
      - `target` — string
      - `events` — array
        - _array of_ `ChannelContextEvent`
          - `id` — string
          - `owner` — string
          - `start` — string
          - `end` — string
          - `summary` — string
          - `attendees` — array
            - _array of_ `ChannelContextEventAttendee`
              - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
    - `kite` — boolean
    - `kiteTarget` — string
    - `kiteVariant` — string
    - `kiteAssign` — string
    - `kiteServiceName` — string
    - `kiteDefaultSubject` — string
    - `service` — string
    - `serviceTitle` — string
    - `serviceRecipient` — string
    - `assignee` — User
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
    - `telephony` — boolean
    - `sms` — boolean
    - `mms` — boolean
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
    - `messagingSenderId` — string
    - `messagingReplyUntil` — number
    - `broadcast` — boolean
    - `external` — boolean
    - `autoRecord` — boolean
    - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
    - `transcriptionLanguage` — string
    - `wizyGuestViewOnly` — boolean
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `channelType` — string **(required)** _(enum: `direct`, `group`)_
    - `memberCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `createdBy` — string **(required)**
    - `updatedAt` — string
  - `event` — CalendarEvent **(required)**
    - `id` — string
    - `owner` — string
    - `start` — string
    - `end` — string
    - `summary` — string
    - `attendees` — array
      - _array of_ `string`
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/kite/calendar/channels/{channelId}/events/{eventOwner}/{eventId}`

Cancels an existing calendar event, optionally providing a reason for cancellation.

- operationId: `CancelCalendarEvent`
- **Scopes**: `kite:CancelCalendarEvent`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or john.doe@example.com). _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `eventId` (path) — string **(required)**
  - `eventOwner` (path) — string **(required)**
  - `reason` (query) — string
- **Response 200** (`CancelCalendarEventResponseContent`)
  - `channel` — Channel **(required)**
    - `subject` — string
    - `description` — string
    - `picture` — string — Picture URL
    - `pictureColor` — string — Picture dominant color represented by a hex value.
    - `access` — string _(enum: `private`, `public`)_
    - `company` — string
    - `context` — ChannelContext
      - `source` — string _(enum: `kite`)_
      - `target` — string
      - `events` — array
        - _array of_ `ChannelContextEvent`
          - `id` — string
          - `owner` — string
          - `start` — string
          - `end` — string
          - `summary` — string
          - `attendees` — array
            - _array of_ `ChannelContextEventAttendee`
              - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
    - `kite` — boolean
    - `kiteTarget` — string
    - `kiteVariant` — string
    - `kiteAssign` — string
    - `kiteServiceName` — string
    - `kiteDefaultSubject` — string
    - `service` — string
    - `serviceTitle` — string
    - `serviceRecipient` — string
    - `assignee` — User
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
    - `telephony` — boolean
    - `sms` — boolean
    - `mms` — boolean
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
    - `messagingSenderId` — string
    - `messagingReplyUntil` — number
    - `broadcast` — boolean
    - `external` — boolean
    - `autoRecord` — boolean
    - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
    - `transcriptionLanguage` — string
    - `wizyGuestViewOnly` — boolean
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `channelType` — string **(required)** _(enum: `direct`, `group`)_
    - `memberCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `createdBy` — string **(required)**
    - `updatedAt` — string
  - `event` — CalendarEvent **(required)**
    - `id` — string
    - `owner` — string
    - `start` — string
    - `end` — string
    - `summary` — string
    - `attendees` — array
      - _array of_ `string`
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/kite/calendar/widgets/{targetId}`

Schedules a new calendar event for a specific Kite widget or agent, creating a conversation channel.

- operationId: `ScheduleCalendarEvent`
- **Scopes**: `kite:ScheduleCalendarEvent`
- **Parameters**
  - `targetId` (path) — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or john.doe@example.com). _(minLen=4; maxLen=200)_
- **Request body** (`application/json` — `ScheduleCalendarEventRequestContent`) **(required)**
  - `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
  - `duration` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])$)_
  - `attendees` — array
    - _array of_ `string`
  - `summary` — string — Event title _(maxLen=255)_
  - `language` — string
  - `timeZone` — string
- **Response 200** (`ScheduleCalendarEventResponseContent`)
  - `channel` — Channel **(required)**
    - `subject` — string
    - `description` — string
    - `picture` — string — Picture URL
    - `pictureColor` — string — Picture dominant color represented by a hex value.
    - `access` — string _(enum: `private`, `public`)_
    - `company` — string
    - `context` — ChannelContext
      - `source` — string _(enum: `kite`)_
      - `target` — string
      - `events` — array
        - _array of_ `ChannelContextEvent`
          - `id` — string
          - `owner` — string
          - `start` — string
          - `end` — string
          - `summary` — string
          - `attendees` — array
            - _array of_ `ChannelContextEventAttendee`
              - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
    - `kite` — boolean
    - `kiteTarget` — string
    - `kiteVariant` — string
    - `kiteAssign` — string
    - `kiteServiceName` — string
    - `kiteDefaultSubject` — string
    - `service` — string
    - `serviceTitle` — string
    - `serviceRecipient` — string
    - `assignee` — User
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
    - `telephony` — boolean
    - `sms` — boolean
    - `mms` — boolean
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
    - `messagingSenderId` — string
    - `messagingReplyUntil` — number
    - `broadcast` — boolean
    - `external` — boolean
    - `autoRecord` — boolean
    - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
    - `transcriptionLanguage` — string
    - `wizyGuestViewOnly` — boolean
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `channelType` — string **(required)** _(enum: `direct`, `group`)_
    - `memberCount` — number **(required)**
    - `createdAt` — string **(required)**
    - `createdBy` — string **(required)**
    - `updatedAt` — string
  - `event` — CalendarEvent **(required)**
    - `id` — string
    - `owner` — string
    - `start` — string
    - `end` — string
    - `summary` — string
    - `attendees` — array
      - _array of_ `string`
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/calendar/widgets/{targetId}/slots`

Retrieves available calendar time slots for a specific Kite widget or agent within the specified date range.

- operationId: `GetCalendarSlots`
- **Scopes**: `kite:GetCalendarSlots`, `kite:read`
- **Parameters**
  - `targetId` (path) — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or john.doe@example.com). _(minLen=4; maxLen=200)_
  - `from` (query) — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])$)_
  - `till` (query) — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])$)_
  - `duration` (query) — string _(minLen=15; maxLen=360)_
  - `timeZone` (query) — string **(required)**
  - `excluded` (query) — string
- **Response 200** (`GetCalendarSlotsResponseContent`)
  - `calendar` — CalendarAvailability **(required)**
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
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/config/{targetId}`

Retrieves the configuration settings for a specific Kite widget or agent, optionally filtered by route.

- operationId: `GetConfig`
- **Scopes**: `kite:GetConfig`, `kite:read`
- **Parameters**
  - `targetId` (path) — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or vadim.ruban@wildix.com). _(minLen=4; maxLen=200)_
  - `route` (query) — string — The unique identifier of the route for time-based configuration.
- **Response 200** (`GetConfigResponseContent`)
  - `config` — KiteConfig **(required)**
    - `targetId` — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or vadim.ruban@wildix.com).
    - `company` — string **(required)** — The unique identifier of the organization widget belongs to (example: it_w119845). _(minLen=3; maxLen=30)_
    - `targetRouteId` — string — The unique identifier of the route for time-based configuration.
    - `targetVariant` — string **(required)** _(enum: `group`, `direct`)_
    - `targetService` — KiteTargetService
      - `uri` — string **(required)**
      - `title` — string **(required)**
    - `agents` — array **(required)**
      - _array of_ `KiteConfigAgent`
        - `id` — string **(required)** _(minLen=12; maxLen=12)_
        - `name` — string
        - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
        - `phone` — string _(pattern=^\+?[0-9]{4,17}$)_
        - `picture` — string
        - `locale` — string
        - `timeZone` — string
        - `company` — string
        - `bot` — boolean
        - `pbxExtension` — string
        - `pbxUserId` — string
        - `pbxGroupId` — string
        - `createdAt` — string
        - `updatedAt` — string
    - `appearance` — WidgetAppearance
      - `pallete` — WidgetPalleteSettings
        - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
        - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `text` — WidgetTextSettings
        - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
        - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
        - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
        - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
    - `welcomeMessages` — array — A list of welcome messages that should be visible to the user.
      - _array of_ `WidgetWelcomeMessage`
        - `text` — string _(minLen=1; maxLen=5000)_
        - `elements` — array
          - _array of_ `Element`
            - _oneOf_ — exactly one of:
              - **`template`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`actions`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`wilma`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `delay` — number — The time in milliseconds until the message will be visible to the end user.
    - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
    - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
    - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
    - `widgetRestrictions` — WidgetRestrictions
      - `anonymous` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
      - `guest` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
    - `features` — array — A list of features that are supported.
      - _array of_ `KiteFeatures`
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/messaging/{channel}/senders`

Retrieves the senders the specified company can send from on one customer messaging channel (the Facebook pages on Messenger, the brands on RCS). kite holds no sender inventory of its own: it proxies classound's list for that channel, an s2s operation the console cannot call with a user token, exactly as ListWhatsAppNumbers proxies classound's number list. The answer is the senders bound to the company, configured or not, so a sender that has never been routed still appears here and can be picked on the configuration screen; a sender that is already routed carries its linked service, and one that is not carries no service at all. A channel whose classound list does not exist yet is refused with a validation error. On RCS only, like ListWhatsAppNumbers, it accepts an x-bees user token as well as a service, PBX or API key token, with the company taken from the user token, because x-bees picks the brand when a user starts an RCS conversation by number; on Messenger it stays privileged. The configuration operations beside it stay privileged.

- operationId: `ListMessagingSenders`
- **Scopes**: `kite:ListMessagingSenders`, `kite:read`
- **Parameters**
  - `channel` (path) — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`ListMessagingSendersResponseContent`)
  - `senders` — array **(required)**
    - _array of_ `MessagingSender`
      - `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
      - `name` — string **(required)** — The sender name as the supplier holds it (the page name on Messenger, the brand id on RCS, which has no name of its own). The member is required, but the value may be an empty string: classound stores and returns an empty name for a sender that was bound without one, and @required does not exclude the empty string. A caller that lists senders should fall back to the sender id when the name is empty.
      - `url` — string — The public URL of the sender. classound sends an empty string when it holds no URL rather than omitting the value, so the member is optional here and an empty string is equally possible; treat both as no URL.
      - `service` — Service
        - `id` — number **(required)**
        - `uri` — string **(required)**
        - `title` — string **(required)**
        - `settings` — ServiceSettings **(required)**
          - `phoneNumber` — string
          - `messagingNumber` — string
        - `extensions` — array **(required)**
          - _array of_ `string`
        - `pbx` — ServicePbx **(required)**
          - `domain` — string **(required)**
          - `port` — number **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/messaging/{channel}/senders/{senderId}/configuration`

Retrieves the routing configuration of a single sender on a customer messaging channel. The sender id is checked against the grammar of the channel named in the path.

- operationId: `GetMessagingSenderConfiguration`
- **Scopes**: `kite:GetMessagingSenderConfiguration`, `kite:read`
- **Parameters**
  - `channel` (path) — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `senderId` (path) — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`GetMessagingSenderConfigurationResponseContent`)
  - `configuration` — MessagingSenderConfig **(required)** — The routing configuration of one sender on a customer messaging channel. It mirrors WhatsAppConfig with the channel and the sender id in place of the service number.
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The specified service is used during conversation creation which means that conversation can be linked to the same service as for phone calls. A sender on these channels carries no phone number, so unlike WhatsApp there is nothing to derive this service from: it is always chosen explicitly.
    - `routes` — array — A list of routes that define different routing rules for the sender. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `MessagingSenderConfigRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `RouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — RouteServiceTarget **(required)**
                - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — RouteAgentTarget **(required)**
                - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — RouteBotTarget **(required)**
                - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — RouteServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — RouteAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — RouteBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/kite/messaging/{channel}/senders/{senderId}/configuration`

Creates or updates the routing configuration of a single sender on a customer messaging channel. The sender id is checked against the grammar of the channel named in the path. The stored row is what the inbound handler of that channel reads to decide where a message goes, so a sender with no configuration is not routable.

- operationId: `PutMessagingSenderConfiguration`
- **Scopes**: `kite:PutMessagingSenderConfiguration`
- **Parameters**
  - `channel` (path) — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `senderId` (path) — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Request body** (`application/json` — `PutMessagingSenderConfigurationRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The specified service is used during conversation creation which means that conversation can be linked to the same service as for phone calls. A sender on these channels carries no phone number, so unlike WhatsApp there is nothing to derive this service from: it is always chosen explicitly.
  - `routes` — array — A list of routes that define different routing rules for the sender. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `MessagingSenderConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _array of_ `RouteRule`
          - _oneOf_ — exactly one of:
            - **`timeFrame`**
              - `timeFrame` — RouteTimeFrameRule **(required)**
                - _(nesting depth limit — see `RouteTimeFrameRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — RouteServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — RouteAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — RouteBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
          - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - `id` — string **(required)** — An ID of the bot.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _array of_ `RouteActionCondition`
          - _oneOf_ — exactly one of:
            - **`replyTimeout`**
              - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReplyTimeoutCondition` in the Schemas appendix)_
            - **`readTimeout`**
              - `readTimeout` — RouteReadTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReadTimeoutCondition` in the Schemas appendix)_
            - **`inactivityTimeout`**
              - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
                - _(nesting depth limit — see `InactivityTimeoutCondition` in the Schemas appendix)_
            - **`evaluation`**
              - `evaluation` — RouteEvaluationCondition **(required)**
                - _(nesting depth limit — see `RouteEvaluationCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`sendMessage`**
            - `sendMessage` — RouteSendMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
          - **`sendGenerativeMessage`**
            - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
          - **`addMembers`**
            - `addMembers` — RouteAddMembersTask **(required)**
              - `emails` — array **(required)**
                - _array of_ `string`
          - **`notifyMessage`**
            - `notifyMessage` — RouteNotifyMessage **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
              - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
          - **`notifyEmail`**
            - `notifyEmail` — RouteNotifyEmail **(required)**
              - `recipient` — string **(required)** — An email where to send the message.
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- **Response 200** (`PutMessagingSenderConfigurationResponseContent`)
  - `configuration` — MessagingSenderConfig **(required)** — The routing configuration of one sender on a customer messaging channel. It mirrors WhatsAppConfig with the channel and the sender id in place of the service number.
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The specified service is used during conversation creation which means that conversation can be linked to the same service as for phone calls. A sender on these channels carries no phone number, so unlike WhatsApp there is nothing to derive this service from: it is always chosen explicitly.
    - `routes` — array — A list of routes that define different routing rules for the sender. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `MessagingSenderConfigRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `RouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — RouteServiceTarget **(required)**
                - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — RouteAgentTarget **(required)**
                - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — RouteBotTarget **(required)**
                - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — RouteServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — RouteAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — RouteBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/services`

Retrieves a list of available services for Kite-based conversations within the specified organization.

- operationId: `ListServices`
- **Scopes**: `kite:ListServices`, `kite:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the organization when a service token is used. _(minLen=3; maxLen=30)_
- **Response 200** (`ListServicesResponseContent`)
  - `services` — array **(required)**
    - _array of_ `Service`
      - `id` — number **(required)**
      - `uri` — string **(required)**
      - `title` — string **(required)**
      - `settings` — ServiceSettings **(required)**
        - `phoneNumber` — string
        - `messagingNumber` — string
      - `extensions` — array **(required)**
        - _array of_ `string`
      - `pbx` — ServicePbx **(required)**
        - `domain` — string **(required)**
        - `port` — number **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/sms/configurations`

Retrieves a list of SMS configurations for all service numbers in the specified company.

- operationId: `ListSmsConfigurations`
- **Scopes**: `kite:ListSmsConfigurations`, `kite:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`ListSmsConfigurationsResponseContent`)
  - `configurations` — array **(required)**
    - _array of_ `SmsConfig`
      - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
      - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
        - _array of_ `SmsConfigRoute`
          - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
          - `rules` — array **(required)** _(minItems=1; maxItems=20)_
            - _array of_ `RouteRule`
              - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
          - `target` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`service`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`agent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`bot`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
            - _array of_ `RouteAction`
              - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — RouteServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — RouteAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — RouteBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `serviceNumber` — string **(required)**
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/sms/configurations/{serviceNumber}`

Retrieves the SMS configuration settings for a specific service number.

- operationId: `GetSmsNumberConfiguration`
- **Scopes**: `kite:GetSmsNumberConfiguration`, `kite:read`
- **Parameters**
  - `serviceNumber` (path) — string **(required)**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`GetSmsNumberConfigurationResponseContent`)
  - `configuration` — SmsConfig **(required)**
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `SmsConfigRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `RouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — RouteServiceTarget **(required)**
                - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — RouteAgentTarget **(required)**
                - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — RouteBotTarget **(required)**
                - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — RouteServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — RouteAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — RouteBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `serviceNumber` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/kite/sms/configurations/{serviceNumber}`

Creates or updates the SMS configuration settings for a specific service number.

- operationId: `PutSmsNumberConfiguration`
- **Scopes**: `kite:PutSmsNumberConfiguration`
- **Parameters**
  - `serviceNumber` (path) — string **(required)**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Request body** (`application/json` — `PutSmsNumberConfigurationRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `SmsConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _array of_ `RouteRule`
          - _oneOf_ — exactly one of:
            - **`timeFrame`**
              - `timeFrame` — RouteTimeFrameRule **(required)**
                - _(nesting depth limit — see `RouteTimeFrameRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — RouteServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — RouteAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — RouteBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
          - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - `id` — string **(required)** — An ID of the bot.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _array of_ `RouteActionCondition`
          - _oneOf_ — exactly one of:
            - **`replyTimeout`**
              - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReplyTimeoutCondition` in the Schemas appendix)_
            - **`readTimeout`**
              - `readTimeout` — RouteReadTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReadTimeoutCondition` in the Schemas appendix)_
            - **`inactivityTimeout`**
              - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
                - _(nesting depth limit — see `InactivityTimeoutCondition` in the Schemas appendix)_
            - **`evaluation`**
              - `evaluation` — RouteEvaluationCondition **(required)**
                - _(nesting depth limit — see `RouteEvaluationCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`sendMessage`**
            - `sendMessage` — RouteSendMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
          - **`sendGenerativeMessage`**
            - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
          - **`addMembers`**
            - `addMembers` — RouteAddMembersTask **(required)**
              - `emails` — array **(required)**
                - _array of_ `string`
          - **`notifyMessage`**
            - `notifyMessage` — RouteNotifyMessage **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
              - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
          - **`notifyEmail`**
            - `notifyEmail` — RouteNotifyEmail **(required)**
              - `recipient` — string **(required)** — An email where to send the message.
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- **Response 200** (`PutSmsNumberConfigurationResponseContent`)
  - `configuration` — SmsConfig **(required)**
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `SmsConfigRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `RouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — RouteServiceTarget **(required)**
                - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — RouteAgentTarget **(required)**
                - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — RouteBotTarget **(required)**
                - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — RouteServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — RouteAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — RouteBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `serviceNumber` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/sms/numbers`

Retrieves a list of available SMS service numbers for the specified company.

- operationId: `ListSmsNumbers`
- **Scopes**: `kite:ListSmsNumbers`, `kite:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`ListSmsNumbersResponseContent`)
  - `numbers` — array **(required)**
    - _array of_ `SmsServiceNumber`
      - `number` — string **(required)** — A phone number registered though Classound.
      - `service` — Service
        - `id` — number **(required)**
        - `uri` — string **(required)**
        - `title` — string **(required)**
        - `settings` — ServiceSettings **(required)**
          - `phoneNumber` — string
          - `messagingNumber` — string
        - `extensions` — array **(required)**
          - _array of_ `string`
        - `pbx` — ServicePbx **(required)**
          - `domain` — string **(required)**
          - `port` — number **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/whatsapp/configurations`

Retrieves a list of WhatsApp configurations for all service numbers in the specified company.

- operationId: `ListWhatsAppConfigurations`
- **Scopes**: `kite:ListWhatsAppConfigurations`, `kite:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`ListWhatsAppConfigurationsResponseContent`)
  - `configurations` — array **(required)**
    - _array of_ `WhatsAppConfig`
      - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
      - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
        - _array of_ `WhatsAppConfigRoute`
          - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
          - `rules` — array **(required)** _(minItems=1; maxItems=20)_
            - _array of_ `RouteRule`
              - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
          - `target` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`service`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`agent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`bot`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
            - _array of_ `RouteAction`
              - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — RouteServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — RouteAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — RouteBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
      - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
      - `serviceNumber` — string **(required)**
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/whatsapp/configurations/{serviceNumber}`

Retrieves the WhatsApp configuration settings for a specific service number.

- operationId: `GetWhatsAppNumberConfiguration`
- **Scopes**: `kite:GetWhatsAppNumberConfiguration`, `kite:read`
- **Parameters**
  - `serviceNumber` (path) — string **(required)**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`GetWhatsAppNumberConfigurationResponseContent`)
  - `configuration` — WhatsAppConfig **(required)**
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WhatsAppConfigRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `RouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — RouteServiceTarget **(required)**
                - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — RouteAgentTarget **(required)**
                - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — RouteBotTarget **(required)**
                - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — RouteServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — RouteAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — RouteBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `serviceNumber` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/kite/whatsapp/configurations/{serviceNumber}`

Creates or updates the WhatsApp configuration settings for a specific service number.

- operationId: `PutWhatsAppNumberConfiguration`
- **Scopes**: `kite:PutWhatsAppNumberConfiguration`
- **Parameters**
  - `serviceNumber` (path) — string **(required)**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Request body** (`application/json` — `PutWhatsAppNumberConfigurationRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WhatsAppConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _array of_ `RouteRule`
          - _oneOf_ — exactly one of:
            - **`timeFrame`**
              - `timeFrame` — RouteTimeFrameRule **(required)**
                - _(nesting depth limit — see `RouteTimeFrameRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — RouteServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — RouteAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — RouteBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
          - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - `id` — string **(required)** — An ID of the bot.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _array of_ `RouteActionCondition`
          - _oneOf_ — exactly one of:
            - **`replyTimeout`**
              - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReplyTimeoutCondition` in the Schemas appendix)_
            - **`readTimeout`**
              - `readTimeout` — RouteReadTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReadTimeoutCondition` in the Schemas appendix)_
            - **`inactivityTimeout`**
              - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
                - _(nesting depth limit — see `InactivityTimeoutCondition` in the Schemas appendix)_
            - **`evaluation`**
              - `evaluation` — RouteEvaluationCondition **(required)**
                - _(nesting depth limit — see `RouteEvaluationCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`sendMessage`**
            - `sendMessage` — RouteSendMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
          - **`sendGenerativeMessage`**
            - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
          - **`addMembers`**
            - `addMembers` — RouteAddMembersTask **(required)**
              - `emails` — array **(required)**
                - _array of_ `string`
          - **`notifyMessage`**
            - `notifyMessage` — RouteNotifyMessage **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
              - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
          - **`notifyEmail`**
            - `notifyEmail` — RouteNotifyEmail **(required)**
              - `recipient` — string **(required)** — An email where to send the message.
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- **Response 200** (`PutWhatsAppNumberConfigurationResponseContent`)
  - `configuration` — WhatsAppConfig **(required)**
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WhatsAppConfigRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `RouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — RouteServiceTarget **(required)**
                - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — RouteAgentTarget **(required)**
                - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — RouteBotTarget **(required)**
                - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — RouteServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — RouteAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — RouteBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `serviceNumber` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/whatsapp/numbers`

Retrieves a list of available WhatsApp service numbers for the specified company.

- operationId: `ListWhatsAppNumbers`
- **Scopes**: `kite:ListWhatsAppNumbers`, `kite:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`ListWhatsAppNumbersResponseContent`)
  - `numbers` — array **(required)**
    - _array of_ `WhatsAppServiceNumber`
      - `number` — string **(required)** — A WhatsApp phone number registered though Classound.
      - `service` — Service
        - `id` — number **(required)**
        - `uri` — string **(required)**
        - `title` — string **(required)**
        - `settings` — ServiceSettings **(required)**
          - `phoneNumber` — string
          - `messagingNumber` — string
        - `extensions` — array **(required)**
          - _array of_ `string`
        - `pbx` — ServicePbx **(required)**
          - `domain` — string **(required)**
          - `port` — number **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/whatsapp/templates/{serviceNumber}`

Retrieves a list of available WhatsApp message templates for a specific service number.

- operationId: `ListWhatsAppTemplates`
- **Scopes**: `kite:ListWhatsAppTemplates`, `kite:read`
- **Parameters**
  - `serviceNumber` (path) — string **(required)**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`ListWhatsAppTemplatesResponseContent`)
  - `templates` — array **(required)**
    - _array of_ `Template`
      - `name` — string **(required)**
      - `parameterFormat` — string **(required)** _(enum: `NAMED`)_
      - `components` — array **(required)**
        - _array of_ `Component`
          - `type` — string **(required)** _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_
          - `format` — string **(required)** _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_
          - `text` — string
          - `example` — ComponentExample
            - `headerHandle` — array
              - _array of_ `string`
            - `bodyTextNamedParams` — array
              - _(nesting depth limit — see `BodyTextNamedParam` in the Schemas appendix)_
          - `buttons` — array
            - _array of_ `Button`
              - _(nesting depth limit — see `Button` in the Schemas appendix)_
      - `language` — string **(required)**
      - `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
      - `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
      - `subCategory` — string
      - `id` — string **(required)**
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/widgets`

Retrieves a list of Kite widgets for the specified company.

- operationId: `ListWidgets`
- **Scopes**: `kite:ListWidgets`, `kite:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Response 200** (`ListWidgetsResponseContent`)
  - `widgets` — array **(required)**
    - _array of_ `Widget`
      - `appearance` — WidgetAppearance
        - `pallete` — WidgetPalleteSettings
          - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
          - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
        - `text` — WidgetTextSettings
          - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
          - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
          - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
          - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
      - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
        - _array of_ `WidgetRoute`
          - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
          - `rules` — array **(required)** _(minItems=1; maxItems=20)_
            - _array of_ `WidgetRouteRule`
              - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
          - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
            - _array of_ `WidgetWelcomeMessage`
              - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
          - `target` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`service`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`agent`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`bot`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
            - _array of_ `RouteAction`
              - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _array of_ `WidgetWelcomeMessage`
          - `text` — string _(minLen=1; maxLen=5000)_
          - `elements` — array
            - _array of_ `Element`
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
          - `delay` — number — The time in milliseconds until the message will be visible to the end user.
      - `name` — string **(required)** _(minLen=1; maxLen=100)_
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — WidgetServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — WidgetAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — WidgetBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
      - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
      - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
      - `widgetRestrictions` — WidgetRestrictions
        - `anonymous` — WidgetRestrictionSet
          - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
          - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
          - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
          - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
          - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
          - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
        - `guest` — WidgetRestrictionSet
          - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
          - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
          - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
          - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
          - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
          - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
      - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
      - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
      - `company` — string **(required)**
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/kite/widgets`

Creates a new widget.

- operationId: `CreateWidget`
- **Scopes**: `kite:CreateWidget`
- **Parameters**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Request body** (`application/json` — `CreateWidgetRequestContent`) **(required)**
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WidgetRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _array of_ `WidgetRouteRule`
          - _oneOf_ — exactly one of:
            - **`timeFrame`**
              - `timeFrame` — WidgetRouteTimeFrameRule **(required)**
                - _(nesting depth limit — see `WidgetRouteTimeFrameRule` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _array of_ `WidgetWelcomeMessage`
          - `text` — string _(minLen=1; maxLen=5000)_
          - `elements` — array
            - _array of_ `Element`
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
          - `delay` — number — The time in milliseconds until the message will be visible to the end user.
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — WidgetServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — WidgetAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — WidgetBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _array of_ `Element`
          - _oneOf_ — exactly one of:
            - **`template`**
              - `template` — MessageTemplateConfig **(required)**
                - _(nesting depth limit — see `MessageTemplateConfig` in the Schemas appendix)_
            - **`actions`**
              - `actions` — array **(required)**
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
            - **`wilma`**
              - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
                - _(nesting depth limit — see `WilmaChatElement` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `name` — string **(required)** _(minLen=1; maxLen=100)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — WidgetServiceTarget **(required)**
          - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
          - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
      - **`agent`**
        - `agent` — WidgetAgentTarget **(required)**
          - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
      - **`bot`**
        - `bot` — WidgetBotTarget **(required)**
          - `id` — string **(required)** — An ID of the bot.
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _array of_ `RouteActionCondition`
          - _oneOf_ — exactly one of:
            - **`replyTimeout`**
              - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReplyTimeoutCondition` in the Schemas appendix)_
            - **`readTimeout`**
              - `readTimeout` — RouteReadTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReadTimeoutCondition` in the Schemas appendix)_
            - **`inactivityTimeout`**
              - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
                - _(nesting depth limit — see `InactivityTimeoutCondition` in the Schemas appendix)_
            - **`evaluation`**
              - `evaluation` — RouteEvaluationCondition **(required)**
                - _(nesting depth limit — see `RouteEvaluationCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`sendMessage`**
            - `sendMessage` — RouteSendMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
          - **`sendGenerativeMessage`**
            - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
          - **`addMembers`**
            - `addMembers` — RouteAddMembersTask **(required)**
              - `emails` — array **(required)**
                - _array of_ `string`
          - **`notifyMessage`**
            - `notifyMessage` — RouteNotifyMessage **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
              - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
          - **`notifyEmail`**
            - `notifyEmail` — RouteNotifyEmail **(required)**
              - `recipient` — string **(required)** — An email where to send the message.
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- **Response 200** (`CreateWidgetResponseContent`)
  - `widget` — Widget **(required)**
    - `appearance` — WidgetAppearance
      - `pallete` — WidgetPalleteSettings
        - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
        - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `text` — WidgetTextSettings
        - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
        - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
        - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
        - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WidgetRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `WidgetRouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
          - _array of_ `WidgetWelcomeMessage`
            - `text` — string _(minLen=1; maxLen=5000)_
            - `elements` — array
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
            - `delay` — number — The time in milliseconds until the message will be visible to the end user.
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — WidgetServiceTarget **(required)**
                - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — WidgetAgentTarget **(required)**
                - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — WidgetBotTarget **(required)**
                - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - `text` — string _(minLen=1; maxLen=5000)_
        - `elements` — array
          - _array of_ `Element`
            - _oneOf_ — exactly one of:
              - **`template`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`actions`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`wilma`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `delay` — number — The time in milliseconds until the message will be visible to the end user.
    - `name` — string **(required)** _(minLen=1; maxLen=100)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — WidgetServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — WidgetAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — WidgetBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
    - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
    - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
    - `widgetRestrictions` — WidgetRestrictions
      - `anonymous` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
      - `guest` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
    - `company` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/kite/widgets/preview`

Creates or updates a temporary widget to assist with configuration testing. Preview widgets mimic the behavior and appearance of regular widgets but are automatically deleted after two hours. They are primarily designed for use in the Kite configuration interface, enabling users to experiment with settings and instantly visualize how changes affect the widget's design and functionality.

- operationId: `CreateOrUpdateWidgetPreview`
- **Scopes**: `kite:CreateOrUpdateWidgetPreview`
- **Parameters**
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Request body** (`application/json` — `CreateOrUpdateWidgetPreviewRequestContent`) **(required)**
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WidgetRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _array of_ `WidgetRouteRule`
          - _oneOf_ — exactly one of:
            - **`timeFrame`**
              - `timeFrame` — WidgetRouteTimeFrameRule **(required)**
                - _(nesting depth limit — see `WidgetRouteTimeFrameRule` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _array of_ `WidgetWelcomeMessage`
          - `text` — string _(minLen=1; maxLen=5000)_
          - `elements` — array
            - _array of_ `Element`
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
          - `delay` — number — The time in milliseconds until the message will be visible to the end user.
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — WidgetServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — WidgetAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — WidgetBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _array of_ `Element`
          - _oneOf_ — exactly one of:
            - **`template`**
              - `template` — MessageTemplateConfig **(required)**
                - _(nesting depth limit — see `MessageTemplateConfig` in the Schemas appendix)_
            - **`actions`**
              - `actions` — array **(required)**
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
            - **`wilma`**
              - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
                - _(nesting depth limit — see `WilmaChatElement` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `name` — string **(required)** _(minLen=1; maxLen=100)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — WidgetServiceTarget **(required)**
          - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
          - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
      - **`agent`**
        - `agent` — WidgetAgentTarget **(required)**
          - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
      - **`bot`**
        - `bot` — WidgetBotTarget **(required)**
          - `id` — string **(required)** — An ID of the bot.
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _array of_ `RouteActionCondition`
          - _oneOf_ — exactly one of:
            - **`replyTimeout`**
              - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReplyTimeoutCondition` in the Schemas appendix)_
            - **`readTimeout`**
              - `readTimeout` — RouteReadTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReadTimeoutCondition` in the Schemas appendix)_
            - **`inactivityTimeout`**
              - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
                - _(nesting depth limit — see `InactivityTimeoutCondition` in the Schemas appendix)_
            - **`evaluation`**
              - `evaluation` — RouteEvaluationCondition **(required)**
                - _(nesting depth limit — see `RouteEvaluationCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`sendMessage`**
            - `sendMessage` — RouteSendMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
          - **`sendGenerativeMessage`**
            - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
          - **`addMembers`**
            - `addMembers` — RouteAddMembersTask **(required)**
              - `emails` — array **(required)**
                - _array of_ `string`
          - **`notifyMessage`**
            - `notifyMessage` — RouteNotifyMessage **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
              - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
          - **`notifyEmail`**
            - `notifyEmail` — RouteNotifyEmail **(required)**
              - `recipient` — string **(required)** — An email where to send the message.
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `temporaryWidgetId` — string **(required)**
- **Response 200** (`CreateOrUpdateWidgetPreviewResponseContent`)
  - `widget` — Widget **(required)**
    - `appearance` — WidgetAppearance
      - `pallete` — WidgetPalleteSettings
        - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
        - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `text` — WidgetTextSettings
        - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
        - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
        - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
        - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WidgetRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `WidgetRouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
          - _array of_ `WidgetWelcomeMessage`
            - `text` — string _(minLen=1; maxLen=5000)_
            - `elements` — array
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
            - `delay` — number — The time in milliseconds until the message will be visible to the end user.
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — WidgetServiceTarget **(required)**
                - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — WidgetAgentTarget **(required)**
                - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — WidgetBotTarget **(required)**
                - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - `text` — string _(minLen=1; maxLen=5000)_
        - `elements` — array
          - _array of_ `Element`
            - _oneOf_ — exactly one of:
              - **`template`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`actions`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`wilma`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `delay` — number — The time in milliseconds until the message will be visible to the end user.
    - `name` — string **(required)** _(minLen=1; maxLen=100)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — WidgetServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — WidgetAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — WidgetBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
    - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
    - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
    - `widgetRestrictions` — WidgetRestrictions
      - `anonymous` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
      - `guest` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
    - `company` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/kite/widgets/{widgetId}`

Retrieves details of a specific widget by its unique identifier.

- operationId: `GetWidget`
- **Scopes**: `kite:GetWidget`, `kite:read`
- **Parameters**
  - `widgetId` (path) — string **(required)** — The unique identifier of the widget. _(pattern=^[0-9a-z]{8}$)_
- **Response 200** (`GetWidgetResponseContent`)
  - `widget` — Widget **(required)**
    - `appearance` — WidgetAppearance
      - `pallete` — WidgetPalleteSettings
        - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
        - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `text` — WidgetTextSettings
        - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
        - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
        - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
        - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WidgetRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `WidgetRouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
          - _array of_ `WidgetWelcomeMessage`
            - `text` — string _(minLen=1; maxLen=5000)_
            - `elements` — array
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
            - `delay` — number — The time in milliseconds until the message will be visible to the end user.
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — WidgetServiceTarget **(required)**
                - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — WidgetAgentTarget **(required)**
                - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — WidgetBotTarget **(required)**
                - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - `text` — string _(minLen=1; maxLen=5000)_
        - `elements` — array
          - _array of_ `Element`
            - _oneOf_ — exactly one of:
              - **`template`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`actions`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`wilma`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `delay` — number — The time in milliseconds until the message will be visible to the end user.
    - `name` — string **(required)** _(minLen=1; maxLen=100)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — WidgetServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — WidgetAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — WidgetBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
    - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
    - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
    - `widgetRestrictions` — WidgetRestrictions
      - `anonymous` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
      - `guest` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
    - `company` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/kite/widgets/{widgetId}`

Updates the configuration of an existing widget.

- operationId: `UpdateWidget`
- **Scopes**: `kite:UpdateWidget`
- **Parameters**
  - `widgetId` (path) — string **(required)** — The unique identifier of the widget to be updated. _(pattern=^[0-9a-z]{8}$)_
  - `company` (query) — string — The unique identifier of the company when a service token is used.
- **Request body** (`application/json` — `UpdateWidgetRequestContent`) **(required)**
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WidgetRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _array of_ `WidgetRouteRule`
          - _oneOf_ — exactly one of:
            - **`timeFrame`**
              - `timeFrame` — WidgetRouteTimeFrameRule **(required)**
                - _(nesting depth limit — see `WidgetRouteTimeFrameRule` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _array of_ `WidgetWelcomeMessage`
          - `text` — string _(minLen=1; maxLen=5000)_
          - `elements` — array
            - _array of_ `Element`
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
          - `delay` — number — The time in milliseconds until the message will be visible to the end user.
      - `target` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`service`**
            - `service` — WidgetServiceTarget **(required)**
              - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
              - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
          - **`agent`**
            - `agent` — WidgetAgentTarget **(required)**
              - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
          - **`bot`**
            - `bot` — WidgetBotTarget **(required)**
              - `id` — string **(required)** — An ID of the bot.
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _array of_ `RouteAction`
          - `id` — string **(required)** _(minLen=6; maxLen=6)_
          - `conditions` — array — List of conditions that must match before making an action.
            - _array of_ `RouteActionCondition`
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
          - `task` — union **(required)**
            - _oneOf_ — exactly one of:
              - **`sendMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`sendGenerativeMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`addMembers`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyMessage`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`notifyEmail`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _array of_ `Element`
          - _oneOf_ — exactly one of:
            - **`template`**
              - `template` — MessageTemplateConfig **(required)**
                - _(nesting depth limit — see `MessageTemplateConfig` in the Schemas appendix)_
            - **`actions`**
              - `actions` — array **(required)**
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
            - **`wilma`**
              - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
                - _(nesting depth limit — see `WilmaChatElement` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `name` — string **(required)** _(minLen=1; maxLen=100)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — WidgetServiceTarget **(required)**
          - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
          - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
      - **`agent`**
        - `agent` — WidgetAgentTarget **(required)**
          - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
      - **`bot`**
        - `bot` — WidgetBotTarget **(required)**
          - `id` — string **(required)** — An ID of the bot.
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _array of_ `RouteActionCondition`
          - _oneOf_ — exactly one of:
            - **`replyTimeout`**
              - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReplyTimeoutCondition` in the Schemas appendix)_
            - **`readTimeout`**
              - `readTimeout` — RouteReadTimeoutCondition **(required)**
                - _(nesting depth limit — see `RouteReadTimeoutCondition` in the Schemas appendix)_
            - **`inactivityTimeout`**
              - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
                - _(nesting depth limit — see `InactivityTimeoutCondition` in the Schemas appendix)_
            - **`evaluation`**
              - `evaluation` — RouteEvaluationCondition **(required)**
                - _(nesting depth limit — see `RouteEvaluationCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`sendMessage`**
            - `sendMessage` — RouteSendMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
          - **`sendGenerativeMessage`**
            - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
          - **`addMembers`**
            - `addMembers` — RouteAddMembersTask **(required)**
              - `emails` — array **(required)**
                - _array of_ `string`
          - **`notifyMessage`**
            - `notifyMessage` — RouteNotifyMessage **(required)**
              - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
              - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
              - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
          - **`notifyEmail`**
            - `notifyEmail` — RouteNotifyEmail **(required)**
              - `recipient` — string **(required)** — An email where to send the message.
              - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
              - `variables` — array — List of generative variables that can be used to customize the email message content.
                - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- **Response 200** (`UpdateWidgetResponseContent`)
  - `widget` — Widget **(required)**
    - `appearance` — WidgetAppearance
      - `pallete` — WidgetPalleteSettings
        - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
        - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `text` — WidgetTextSettings
        - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
        - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
        - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
        - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WidgetRoute`
        - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
        - `rules` — array **(required)** _(minItems=1; maxItems=20)_
          - _array of_ `WidgetRouteRule`
            - _oneOf_ — exactly one of:
              - **`timeFrame`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
          - _array of_ `WidgetWelcomeMessage`
            - `text` — string _(minLen=1; maxLen=5000)_
            - `elements` — array
              - _(nesting depth limit — see `Element` in the Schemas appendix)_
            - `delay` — number — The time in milliseconds until the message will be visible to the end user.
        - `target` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`service`**
              - `service` — WidgetServiceTarget **(required)**
                - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
            - **`agent`**
              - `agent` — WidgetAgentTarget **(required)**
                - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
            - **`bot`**
              - `bot` — WidgetBotTarget **(required)**
                - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
        - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
          - _array of_ `RouteAction`
            - `id` — string **(required)** _(minLen=6; maxLen=6)_
            - `conditions` — array — List of conditions that must match before making an action.
              - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
            - `task` — union **(required)**
              - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
            - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - `text` — string _(minLen=1; maxLen=5000)_
        - `elements` — array
          - _array of_ `Element`
            - _oneOf_ — exactly one of:
              - **`template`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`actions`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`wilma`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `delay` — number — The time in milliseconds until the message will be visible to the end user.
    - `name` — string **(required)** _(minLen=1; maxLen=100)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - `service` — WidgetServiceTarget **(required)**
            - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
            - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
        - **`agent`**
          - `agent` — WidgetAgentTarget **(required)**
            - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
        - **`bot`**
          - `bot` — WidgetBotTarget **(required)**
            - `id` — string **(required)** — An ID of the bot.
    - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
    - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
    - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
    - `widgetRestrictions` — WidgetRestrictions
      - `anonymous` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
      - `guest` — WidgetRestrictionSet
        - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
        - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
        - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
        - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
        - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
        - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - `id` — string **(required)** _(minLen=6; maxLen=6)_
        - `conditions` — array — List of conditions that must match before making an action.
          - _array of_ `RouteActionCondition`
            - _oneOf_ — exactly one of:
              - **`replyTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`readTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`inactivityTimeout`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
              - **`evaluation`**
                - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - `task` — union **(required)**
          - _oneOf_ — exactly one of:
            - **`sendMessage`**
              - `sendMessage` — RouteSendMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendMessageTask` in the Schemas appendix)_
            - **`sendGenerativeMessage`**
              - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
                - _(nesting depth limit — see `RouteSendGenerativeMessageTask` in the Schemas appendix)_
            - **`addMembers`**
              - `addMembers` — RouteAddMembersTask **(required)**
                - _(nesting depth limit — see `RouteAddMembersTask` in the Schemas appendix)_
            - **`notifyMessage`**
              - `notifyMessage` — RouteNotifyMessage **(required)**
                - _(nesting depth limit — see `RouteNotifyMessage` in the Schemas appendix)_
            - **`notifyEmail`**
              - `notifyEmail` — RouteNotifyEmail **(required)**
                - _(nesting depth limit — see `RouteNotifyEmail` in the Schemas appendix)_
        - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
    - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
    - `company` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/kite/widgets/{widgetId}`

Deletes an existing widget. This operation is idempotent, meaning that if the widget does not exist, the operation will still return a successful response.

- operationId: `DeleteWidget`
- **Scopes**: `kite:DeleteWidget`
- **Parameters**
  - `widgetId` (path) — string **(required)** — The unique identifier of the widget. _(pattern=^[0-9a-z]{8}$)_
- Errors: `400`, `403`, `404`, `429`

### Schemas appendix — Kite API

<details><summary>134 component schemas</summary>

**`ActionElement`**

- _oneOf_ — exactly one of:
  - **`button`**
    - `button` — ButtonElement **(required)**
      - `text` — string **(required)** _(minLen=1; maxLen=96)_
      - `handler` — union **(required)**
        - _oneOf_ — exactly one of:
          - **`link`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`reply`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
          - **`action`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
      - `variant` — string _(enum: `contained`, `outlined`)_
      - `disabled` — boolean

**`BodyTextNamedParam`**

- `paramName` — string **(required)**
- `example` — string **(required)**

**`Button`**

- `type` — string **(required)** _(enum: `QUICK_REPLY`, `URL`, `PHONE_NUMBER`, `OTP`, `MPM`, `CATALOG`, `FLOW`, `VOICE_CALL`, `APP`)_
- `text` — string **(required)** _(maxLen=1024)_
- `flowId` — number
- `flowAction` — string
- `navigateScreen` — string

**`ButtonActionHandler`**

- `id` — string **(required)** — A unique ID of the action within the message. _(minLen=1; maxLen=32)_

**`ButtonElement`**

- `text` — string **(required)** _(minLen=1; maxLen=96)_
- `handler` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`link`**
      - `link` — ButtonLinkHandler **(required)**
        - `url` — string **(required)** _(minLen=3; maxLen=2048)_
    - **`reply`**
      - `reply` — ButtonReplyHandler **(required)**
        - `text` — string _(minLen=1; maxLen=128)_
    - **`action`**
      - `action` — ButtonActionHandler **(required)**
        - `id` — string **(required)** — A unique ID of the action within the message. _(minLen=1; maxLen=32)_
- `variant` — string _(enum: `contained`, `outlined`)_
- `disabled` — boolean

**`ButtonHandler`**

- _oneOf_ — exactly one of:
  - **`link`**
    - `link` — ButtonLinkHandler **(required)**
      - `url` — string **(required)** _(minLen=3; maxLen=2048)_
  - **`reply`**
    - `reply` — ButtonReplyHandler **(required)**
      - `text` — string _(minLen=1; maxLen=128)_
  - **`action`**
    - `action` — ButtonActionHandler **(required)**
      - `id` — string **(required)** — A unique ID of the action within the message. _(minLen=1; maxLen=32)_

**`ButtonLinkHandler`**

- `url` — string **(required)** _(minLen=3; maxLen=2048)_

**`ButtonReplyHandler`**

- `text` — string _(minLen=1; maxLen=128)_

**`ButtonType`**

- string _(enum: `QUICK_REPLY`, `URL`, `PHONE_NUMBER`, `OTP`, `MPM`, `CATALOG`, `FLOW`, `VOICE_CALL`, `APP`)_

**`ButtonVariant`**

- string _(enum: `contained`, `outlined`)_

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

- `id` — string
- `owner` — string
- `start` — string
- `end` — string
- `summary` — string
- `attendees` — array
  - _array of_ `string`

**`CalendarSlot`**

- `startTime` — string

**`CancelCalendarEventResponseContent`**

- `channel` — Channel **(required)**
  - `subject` — string
  - `description` — string
  - `picture` — string — Picture URL
  - `pictureColor` — string — Picture dominant color represented by a hex value.
  - `access` — string _(enum: `private`, `public`)_
  - `company` — string
  - `context` — ChannelContext
    - `source` — string _(enum: `kite`)_
    - `target` — string
    - `events` — array
      - _array of_ `ChannelContextEvent`
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
    - `ptt` — ChannelContextPushToTalk
      - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
  - `kite` — boolean
  - `kiteTarget` — string
  - `kiteVariant` — string
  - `kiteAssign` — string
  - `kiteServiceName` — string
  - `kiteDefaultSubject` — string
  - `service` — string
  - `serviceTitle` — string
  - `serviceRecipient` — string
  - `assignee` — User
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
  - `telephony` — boolean
  - `sms` — boolean
  - `mms` — boolean
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
  - `messagingSenderId` — string
  - `messagingReplyUntil` — number
  - `broadcast` — boolean
  - `external` — boolean
  - `autoRecord` — boolean
  - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
  - `transcriptionLanguage` — string
  - `wizyGuestViewOnly` — boolean
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `channelType` — string **(required)** _(enum: `direct`, `group`)_
  - `memberCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `createdBy` — string **(required)**
  - `updatedAt` — string
- `event` — CalendarEvent **(required)**
  - `id` — string
  - `owner` — string
  - `start` — string
  - `end` — string
  - `summary` — string
  - `attendees` — array
    - _array of_ `string`

**`Channel`**

- `subject` — string
- `description` — string
- `picture` — string — Picture URL
- `pictureColor` — string — Picture dominant color represented by a hex value.
- `access` — string _(enum: `private`, `public`)_
- `company` — string
- `context` — ChannelContext
  - `source` — string _(enum: `kite`)_
  - `target` — string
  - `events` — array
    - _array of_ `ChannelContextEvent`
      - `id` — string
      - `owner` — string
      - `start` — string
      - `end` — string
      - `summary` — string
      - `attendees` — array
        - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
  - `ptt` — ChannelContextPushToTalk
    - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
- `kite` — boolean
- `kiteTarget` — string
- `kiteVariant` — string
- `kiteAssign` — string
- `kiteServiceName` — string
- `kiteDefaultSubject` — string
- `service` — string
- `serviceTitle` — string
- `serviceRecipient` — string
- `assignee` — User
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
- `telephony` — boolean
- `sms` — boolean
- `mms` — boolean
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `24h_channel_closed`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
- `messagingSenderId` — string
- `messagingReplyUntil` — number
- `broadcast` — boolean
- `external` — boolean
- `autoRecord` — boolean
- `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
- `transcriptionLanguage` — string
- `wizyGuestViewOnly` — boolean
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `channelType` — string **(required)** _(enum: `direct`, `group`)_
- `memberCount` — number **(required)**
- `createdAt` — string **(required)**
- `createdBy` — string **(required)**
- `updatedAt` — string

**`ChannelAccess`**

- string _(enum: `private`, `public`)_

**`ChannelContext`**

- `source` — string _(enum: `kite`)_
- `target` — string
- `events` — array
  - _array of_ `ChannelContextEvent`
    - `id` — string
    - `owner` — string
    - `start` — string
    - `end` — string
    - `summary` — string
    - `attendees` — array
      - _array of_ `ChannelContextEventAttendee`
        - _(nesting depth limit — see `ChannelContextEventAttendee` in the Schemas appendix)_
- `ptt` — ChannelContextPushToTalk
  - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.

**`ChannelContextEvent`**

- `id` — string
- `owner` — string
- `start` — string
- `end` — string
- `summary` — string
- `attendees` — array
  - _array of_ `ChannelContextEventAttendee`
    - `email` — string **(required)**
    - `name` — string
    - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`ChannelContextEventAttendee`**

- `email` — string **(required)**
- `name` — string
- `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`ChannelContextEventAttendeeStatus`**

- string _(enum: `accepted`, `tentative`, `declined`, `none`)_

**`ChannelContextPushToTalk`**

- `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.

**`ChannelContextSource`**

- string _(enum: `kite`)_

**`ChannelMessagingStatus`**

_Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window._

- string _(enum: `window_closed`)_

**`ChannelType`**

- string _(enum: `direct`, `group`)_

**`ChannelWhatsAppStatus`**

- string _(enum: `24h_channel_closed`)_

**`ChatVerbosity`**

_How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text._

- string _(enum: `none`, `simple`, `full`)_

**`Component`**

- `type` — string **(required)** _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_
- `format` — string **(required)** _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_
- `text` — string
- `example` — ComponentExample
  - `headerHandle` — array
    - _array of_ `string`
  - `bodyTextNamedParams` — array
    - _array of_ `BodyTextNamedParam`
      - `paramName` — string **(required)**
      - `example` — string **(required)**
- `buttons` — array
  - _array of_ `Button`
    - `type` — string **(required)** _(enum: `QUICK_REPLY`, `URL`, `PHONE_NUMBER`, `OTP`, `MPM`, `CATALOG`, `FLOW`, `VOICE_CALL`, `APP`)_
    - `text` — string **(required)** _(maxLen=1024)_
    - `flowId` — number
    - `flowAction` — string
    - `navigateScreen` — string

**`ComponentExample`**

- `headerHandle` — array
  - _array of_ `string`
- `bodyTextNamedParams` — array
  - _array of_ `BodyTextNamedParam`
    - `paramName` — string **(required)**
    - `example` — string **(required)**

**`ComponentFormat`**

- string _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_

**`ComponentType`**

- string _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_

**`CreateOrUpdateWidgetPreviewRequestContent`**

- `appearance` — WidgetAppearance
  - `pallete` — WidgetPalleteSettings
    - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
  - `text` — WidgetTextSettings
    - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
    - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
    - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
    - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `WidgetRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `WidgetRouteRule`
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
  - _array of_ `WidgetWelcomeMessage`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `delay` — number — The time in milliseconds until the message will be visible to the end user.
- `name` — string **(required)** _(minLen=1; maxLen=100)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — WidgetServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — WidgetAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — WidgetBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
- `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
- `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
- `widgetRestrictions` — WidgetRestrictions
  - `anonymous` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `guest` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
- `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- `temporaryWidgetId` — string **(required)**

**`CreateOrUpdateWidgetPreviewResponseContent`**

- `widget` — Widget **(required)**
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WidgetRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `WidgetTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `name` — string **(required)** _(minLen=1; maxLen=100)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — WidgetServiceTarget **(required)**
          - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — WidgetAgentTarget **(required)**
          - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — WidgetBotTarget **(required)**
          - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
  - `company` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`CreateWidgetRequestContent`**

- `appearance` — WidgetAppearance
  - `pallete` — WidgetPalleteSettings
    - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
  - `text` — WidgetTextSettings
    - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
    - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
    - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
    - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `WidgetRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `WidgetRouteRule`
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
  - _array of_ `WidgetWelcomeMessage`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `delay` — number — The time in milliseconds until the message will be visible to the end user.
- `name` — string **(required)** _(minLen=1; maxLen=100)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — WidgetServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — WidgetAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — WidgetBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
- `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
- `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
- `widgetRestrictions` — WidgetRestrictions
  - `anonymous` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `guest` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
- `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`CreateWidgetResponseContent`**

- `widget` — Widget **(required)**
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WidgetRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `WidgetTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `name` — string **(required)** _(minLen=1; maxLen=100)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — WidgetServiceTarget **(required)**
          - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — WidgetAgentTarget **(required)**
          - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — WidgetBotTarget **(required)**
          - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
  - `company` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`Element`**

- _oneOf_ — exactly one of:
  - **`template`**
    - `template` — MessageTemplateConfig **(required)**
      - `whatsapp` — TemplateWithParameters
        - `name` — string **(required)**
        - `parameters` — array
          - _(nesting depth limit — see `TemplateParameter` in the Schemas appendix)_
  - **`actions`**
    - `actions` — array **(required)**
      - _array of_ `ActionElement`
        - _oneOf_ — exactly one of:
          - **`button`**
            - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
  - **`wilma`**
    - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
      - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
      - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
      - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
      - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
      - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
      - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
        - `outcome` — string **(required)** — How the turn ended. _(enum: `done`, `stopped`, `failed`)_
        - `durationMs` — number — From the turn's start to its end. Absent when the turn had not ended.
        - `toolCount` — number **(required)** — Steps the turn took, counted as the Wilma assistant counts its work steps: each tool call and each sandbox step (`SandboxStartedEvent`, `SandboxFailedEvent`).
        - `failedCount` — number **(required)** — Steps that failed: calls that failed, including those the stop or failure cut off, and sandbox steps that failed.
      - `artifacts` — array
        - _array of_ `WilmaChatArtifact`
          - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetCalendarSlotsResponseContent`**

- `calendar` — CalendarAvailability **(required)**
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

**`GetConfigResponseContent`**

- `config` — KiteConfig **(required)**
  - `targetId` — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or vadim.ruban@wildix.com).
  - `company` — string **(required)** — The unique identifier of the organization widget belongs to (example: it_w119845). _(minLen=3; maxLen=30)_
  - `targetRouteId` — string — The unique identifier of the route for time-based configuration.
  - `targetVariant` — string **(required)** _(enum: `group`, `direct`)_
  - `targetService` — KiteTargetService
    - `uri` — string **(required)**
    - `title` — string **(required)**
  - `agents` — array **(required)**
    - _array of_ `KiteConfigAgent`
      - `id` — string **(required)** _(minLen=12; maxLen=12)_
      - `name` — string
      - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string _(pattern=^\+?[0-9]{4,17}$)_
      - `picture` — string
      - `locale` — string
      - `timeZone` — string
      - `company` — string
      - `bot` — boolean
      - `pbxExtension` — string
      - `pbxUserId` — string
      - `pbxGroupId` — string
      - `createdAt` — string
      - `updatedAt` — string
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `welcomeMessages` — array — A list of welcome messages that should be visible to the user.
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `features` — array — A list of features that are supported.
    - _array of_ `KiteFeatures`

**`GetMessagingSenderConfigurationResponseContent`**

- `configuration` — MessagingSenderConfig **(required)** — The routing configuration of one sender on a customer messaging channel. It mirrors WhatsAppConfig with the channel and the sender id in place of the service number.
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The specified service is used during conversation creation which means that conversation can be linked to the same service as for phone calls. A sender on these channels carries no phone number, so unlike WhatsApp there is nothing to derive this service from: it is always chosen explicitly.
  - `routes` — array — A list of routes that define different routing rules for the sender. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `MessagingSenderConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `RouteTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetSmsNumberConfigurationResponseContent`**

- `configuration` — SmsConfig **(required)**
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `SmsConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `RouteTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `serviceNumber` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetWhatsAppNumberConfigurationResponseContent`**

- `configuration` — WhatsAppConfig **(required)**
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WhatsAppConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `RouteTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `serviceNumber` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetWidgetResponseContent`**

- `widget` — Widget **(required)**
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WidgetRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `WidgetTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `name` — string **(required)** _(minLen=1; maxLen=100)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — WidgetServiceTarget **(required)**
          - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — WidgetAgentTarget **(required)**
          - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — WidgetBotTarget **(required)**
          - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
  - `company` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`InactivityTimeoutCondition`**

- `timeout` — number **(required)** — Timeout in seconds since last activity in the channel. _(min=1; max=86400)_

**`KiteConfig`**

- `targetId` — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or vadim.ruban@wildix.com).
- `company` — string **(required)** — The unique identifier of the organization widget belongs to (example: it_w119845). _(minLen=3; maxLen=30)_
- `targetRouteId` — string — The unique identifier of the route for time-based configuration.
- `targetVariant` — string **(required)** _(enum: `group`, `direct`)_
- `targetService` — KiteTargetService
  - `uri` — string **(required)**
  - `title` — string **(required)**
- `agents` — array **(required)**
  - _array of_ `KiteConfigAgent`
    - `id` — string **(required)** _(minLen=12; maxLen=12)_
    - `name` — string
    - `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string _(pattern=^\+?[0-9]{4,17}$)_
    - `picture` — string
    - `locale` — string
    - `timeZone` — string
    - `company` — string
    - `bot` — boolean
    - `pbxExtension` — string
    - `pbxUserId` — string
    - `pbxGroupId` — string
    - `createdAt` — string
    - `updatedAt` — string
- `appearance` — WidgetAppearance
  - `pallete` — WidgetPalleteSettings
    - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
  - `text` — WidgetTextSettings
    - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
    - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
    - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
    - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
- `welcomeMessages` — array — A list of welcome messages that should be visible to the user.
  - _array of_ `WidgetWelcomeMessage`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `delay` — number — The time in milliseconds until the message will be visible to the end user.
- `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
- `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
- `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
- `widgetRestrictions` — WidgetRestrictions
  - `anonymous` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `guest` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
- `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
- `features` — array — A list of features that are supported.
  - _array of_ `KiteFeatures`

**`KiteConfigAgent`**

- `id` — string **(required)** _(minLen=12; maxLen=12)_
- `name` — string
- `email` — string _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string _(pattern=^\+?[0-9]{4,17}$)_
- `picture` — string
- `locale` — string
- `timeZone` — string
- `company` — string
- `bot` — boolean
- `pbxExtension` — string
- `pbxUserId` — string
- `pbxGroupId` — string
- `createdAt` — string
- `updatedAt` — string

**`KiteFeatures`**

- string _(enum: `scheduling`)_

**`KiteTargetService`**

- `uri` — string **(required)**
- `title` — string **(required)**

**`KiteVariant`**

- string _(enum: `group`, `direct`)_

**`ListAgentsFilter`**

- _oneOf_ — exactly one of:
  - **`service`**
    - `service` — string **(required)** — The unique identifier of the service which represent URI (example - 2@example.wildixin.com:443).
  - **`extensions`**
    - `extensions` — array **(required)** — A list of extensions that could be used inside Kite based conversation.
      - _array of_ `string`
  - **`emails`**
    - `emails` — array **(required)** — A list of emails that could be used inside Kite based conversation.
      - _array of_ `string`

**`ListAgentsRequestContent`**

- `filter` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — string **(required)** — The unique identifier of the service which represent URI (example - 2@example.wildixin.com:443).
    - **`extensions`**
      - `extensions` — array **(required)** — A list of extensions that could be used inside Kite based conversation.
        - _array of_ `string`
    - **`emails`**
      - `emails` — array **(required)** — A list of emails that could be used inside Kite based conversation.
        - _array of_ `string`

**`ListAgentsResponseContent`**

- `users` — array **(required)**
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

**`ListMessagingSendersResponseContent`**

- `senders` — array **(required)**
  - _array of_ `MessagingSender`
    - `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
    - `name` — string **(required)** — The sender name as the supplier holds it (the page name on Messenger, the brand id on RCS, which has no name of its own). The member is required, but the value may be an empty string: classound stores and returns an empty name for a sender that was bound without one, and @required does not exclude the empty string. A caller that lists senders should fall back to the sender id when the name is empty.
    - `url` — string — The public URL of the sender. classound sends an empty string when it holds no URL rather than omitting the value, so the member is optional here and an empty string is equally possible; treat both as no URL.
    - `service` — Service
      - `id` — number **(required)**
      - `uri` — string **(required)**
      - `title` — string **(required)**
      - `settings` — ServiceSettings **(required)**
        - _(nesting depth limit — see `ServiceSettings` in the Schemas appendix)_
      - `extensions` — array **(required)**
        - _array of_ `string`
      - `pbx` — ServicePbx **(required)**
        - _(nesting depth limit — see `ServicePbx` in the Schemas appendix)_

**`ListServicesResponseContent`**

- `services` — array **(required)**
  - _array of_ `Service`
    - `id` — number **(required)**
    - `uri` — string **(required)**
    - `title` — string **(required)**
    - `settings` — ServiceSettings **(required)**
      - `phoneNumber` — string
      - `messagingNumber` — string
    - `extensions` — array **(required)**
      - _array of_ `string`
    - `pbx` — ServicePbx **(required)**
      - `domain` — string **(required)**
      - `port` — number **(required)**

**`ListSmsConfigurationsResponseContent`**

- `configurations` — array **(required)**
  - _array of_ `SmsConfig`
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `SmsConfigRoute`
        - _(nesting depth limit — see `SmsConfigRoute` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `serviceNumber` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`ListSmsNumbersResponseContent`**

- `numbers` — array **(required)**
  - _array of_ `SmsServiceNumber`
    - `number` — string **(required)** — A phone number registered though Classound.
    - `service` — Service
      - `id` — number **(required)**
      - `uri` — string **(required)**
      - `title` — string **(required)**
      - `settings` — ServiceSettings **(required)**
        - _(nesting depth limit — see `ServiceSettings` in the Schemas appendix)_
      - `extensions` — array **(required)**
        - _array of_ `string`
      - `pbx` — ServicePbx **(required)**
        - _(nesting depth limit — see `ServicePbx` in the Schemas appendix)_

**`ListWhatsAppConfigurationsResponseContent`**

- `configurations` — array **(required)**
  - _array of_ `WhatsAppConfig`
    - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WhatsAppConfigRoute`
        - _(nesting depth limit — see `WhatsAppConfigRoute` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
    - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
    - `serviceNumber` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`ListWhatsAppNumbersResponseContent`**

- `numbers` — array **(required)**
  - _array of_ `WhatsAppServiceNumber`
    - `number` — string **(required)** — A WhatsApp phone number registered though Classound.
    - `service` — Service
      - `id` — number **(required)**
      - `uri` — string **(required)**
      - `title` — string **(required)**
      - `settings` — ServiceSettings **(required)**
        - _(nesting depth limit — see `ServiceSettings` in the Schemas appendix)_
      - `extensions` — array **(required)**
        - _array of_ `string`
      - `pbx` — ServicePbx **(required)**
        - _(nesting depth limit — see `ServicePbx` in the Schemas appendix)_

**`ListWhatsAppTemplatesResponseContent`**

- `templates` — array **(required)**
  - _array of_ `Template`
    - `name` — string **(required)**
    - `parameterFormat` — string **(required)** _(enum: `NAMED`)_
    - `components` — array **(required)**
      - _array of_ `Component`
        - _(nesting depth limit — see `Component` in the Schemas appendix)_
    - `language` — string **(required)**
    - `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
    - `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
    - `subCategory` — string
    - `id` — string **(required)**

**`ListWidgetsResponseContent`**

- `widgets` — array **(required)**
  - _array of_ `Widget`
    - `appearance` — WidgetAppearance
      - `pallete` — WidgetPalleteSettings
        - _(nesting depth limit — see `WidgetPalleteSettings` in the Schemas appendix)_
      - `text` — WidgetTextSettings
        - _(nesting depth limit — see `WidgetTextSettings` in the Schemas appendix)_
    - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
      - _array of_ `WidgetRoute`
        - _(nesting depth limit — see `WidgetRoute` in the Schemas appendix)_
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
    - `name` — string **(required)** _(minLen=1; maxLen=100)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
    - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
    - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
    - `widgetRestrictions` — WidgetRestrictions
      - `anonymous` — WidgetRestrictionSet
        - _(nesting depth limit — see `WidgetRestrictionSet` in the Schemas appendix)_
      - `guest` — WidgetRestrictionSet
        - _(nesting depth limit — see `WidgetRestrictionSet` in the Schemas appendix)_
    - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
    - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
    - `company` — string **(required)**
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`MessageTemplateConfig`**

- `whatsapp` — TemplateWithParameters
  - `name` — string **(required)**
  - `parameters` — array
    - _array of_ `TemplateParameter`
      - `name` — string **(required)**
      - `value` — string **(required)**

**`MessagingChannel`**

_A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number._

- string _(enum: `messenger`, `instagram`, `rcs`)_

**`MessagingSender`**

_One sender the company can send from on a customer messaging channel, as classound reports it (on Messenger, /v1/s2s/messenger/pages; on RCS, /v1/s2s/rcs/brands), with the linked service kite resolves from the sender's own routing configuration._

- `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
- `name` — string **(required)** — The sender name as the supplier holds it (the page name on Messenger, the brand id on RCS, which has no name of its own). The member is required, but the value may be an empty string: classound stores and returns an empty name for a sender that was bound without one, and @required does not exclude the empty string. A caller that lists senders should fall back to the sender id when the name is empty.
- `url` — string — The public URL of the sender. classound sends an empty string when it holds no URL rather than omitting the value, so the member is optional here and an empty string is equally possible; treat both as no URL.
- `service` — Service
  - `id` — number **(required)**
  - `uri` — string **(required)**
  - `title` — string **(required)**
  - `settings` — ServiceSettings **(required)**
    - `phoneNumber` — string
    - `messagingNumber` — string
  - `extensions` — array **(required)**
    - _array of_ `string`
  - `pbx` — ServicePbx **(required)**
    - `domain` — string **(required)**
    - `port` — number **(required)**

**`MessagingSenderConfig`**

_The routing configuration of one sender on a customer messaging channel. It mirrors WhatsAppConfig with the channel and the sender id in place of the service number._

- `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The specified service is used during conversation creation which means that conversation can be linked to the same service as for phone calls. A sender on these channels carries no phone number, so unlike WhatsApp there is nothing to derive this service from: it is always chosen explicitly.
- `routes` — array — A list of routes that define different routing rules for the sender. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `MessagingSenderConfigRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `RouteRule`
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`MessagingSenderConfigRoute`**

- `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
- `rules` — array **(required)** _(minItems=1; maxItems=20)_
  - _array of_ `RouteRule`
    - _oneOf_ — exactly one of:
      - **`timeFrame`**
        - `timeFrame` — RouteTimeFrameRule **(required)**
          - _(nesting depth limit — see `RouteTimeFrameRule` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`NotFoundExceptionResponseContent`**

- `message` — string **(required)** _(default=Not found)_

**`ParameterFormat`**

- string _(enum: `NAMED`)_

**`PutMessagingSenderConfigurationRequestContent`**

- `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The specified service is used during conversation creation which means that conversation can be linked to the same service as for phone calls. A sender on these channels carries no phone number, so unlike WhatsApp there is nothing to derive this service from: it is always chosen explicitly.
- `routes` — array — A list of routes that define different routing rules for the sender. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `MessagingSenderConfigRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `RouteRule`
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`PutMessagingSenderConfigurationResponseContent`**

- `configuration` — MessagingSenderConfig **(required)** — The routing configuration of one sender on a customer messaging channel. It mirrors WhatsAppConfig with the channel and the sender id in place of the service number.
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The specified service is used during conversation creation which means that conversation can be linked to the same service as for phone calls. A sender on these channels carries no phone number, so unlike WhatsApp there is nothing to derive this service from: it is always chosen explicitly.
  - `routes` — array — A list of routes that define different routing rules for the sender. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `MessagingSenderConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `RouteTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `senderId` — string **(required)** — The business side of a customer messaging channel: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. The model only keeps it safe to carry in a URL path; the grammar of each channel is checked by kite against the channel named in the same request (Messenger: 4 to 32 decimal digits, the grammar classound enforces when a page is bound to a company; RCS: the whole pattern below, which is the grammar classound enforces when a brand is bound), so a value outside that grammar can never match a configured sender. It is not a phone number: it is never normalised, and no country prefix is ever added to it or stripped from it. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`PutSmsNumberConfigurationRequestContent`**

- `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `SmsConfigRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `RouteRule`
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`PutSmsNumberConfigurationResponseContent`**

- `configuration` — SmsConfig **(required)**
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `SmsConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `RouteTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `serviceNumber` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`PutWhatsAppNumberConfigurationRequestContent`**

- `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `WhatsAppConfigRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `RouteRule`
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`PutWhatsAppNumberConfigurationResponseContent`**

- `configuration` — WhatsAppConfig **(required)**
  - `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WhatsAppConfigRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `RouteTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — RouteServiceTarget **(required)**
          - _(nesting depth limit — see `RouteServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — RouteAgentTarget **(required)**
          - _(nesting depth limit — see `RouteAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — RouteBotTarget **(required)**
          - _(nesting depth limit — see `RouteBotTarget` in the Schemas appendix)_
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `companyId` — string **(required)** _(minLen=3; maxLen=30)_
  - `serviceNumber` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`RateLimitExceededExceptionResponseContent`**

- `message` — string **(required)** _(default=Too Many Requests)_

**`RescheduleCalendarEventRequestContent`**

- `start` — string _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
- `duration` — string _(minLen=15; maxLen=360)_
- `reason` — string
- `summary` — string — Event title _(maxLen=255)_
- `attendees` — array
  - _array of_ `string`
- `changed` — array
  - _array of_ `string`

**`RescheduleCalendarEventResponseContent`**

- `channel` — Channel **(required)**
  - `subject` — string
  - `description` — string
  - `picture` — string — Picture URL
  - `pictureColor` — string — Picture dominant color represented by a hex value.
  - `access` — string _(enum: `private`, `public`)_
  - `company` — string
  - `context` — ChannelContext
    - `source` — string _(enum: `kite`)_
    - `target` — string
    - `events` — array
      - _array of_ `ChannelContextEvent`
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
    - `ptt` — ChannelContextPushToTalk
      - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
  - `kite` — boolean
  - `kiteTarget` — string
  - `kiteVariant` — string
  - `kiteAssign` — string
  - `kiteServiceName` — string
  - `kiteDefaultSubject` — string
  - `service` — string
  - `serviceTitle` — string
  - `serviceRecipient` — string
  - `assignee` — User
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
  - `telephony` — boolean
  - `sms` — boolean
  - `mms` — boolean
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
  - `messagingSenderId` — string
  - `messagingReplyUntil` — number
  - `broadcast` — boolean
  - `external` — boolean
  - `autoRecord` — boolean
  - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
  - `transcriptionLanguage` — string
  - `wizyGuestViewOnly` — boolean
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `channelType` — string **(required)** _(enum: `direct`, `group`)_
  - `memberCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `createdBy` — string **(required)**
  - `updatedAt` — string
- `event` — CalendarEvent **(required)**
  - `id` — string
  - `owner` — string
  - `start` — string
  - `end` — string
  - `summary` — string
  - `attendees` — array
    - _array of_ `string`

**`RouteAction`**

- `id` — string **(required)** _(minLen=6; maxLen=6)_
- `conditions` — array — List of conditions that must match before making an action.
  - _array of_ `RouteActionCondition`
    - _oneOf_ — exactly one of:
      - **`replyTimeout`**
        - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
          - _(nesting depth limit — see `RouteReplyTimeoutCondition` in the Schemas appendix)_
      - **`readTimeout`**
        - `readTimeout` — RouteReadTimeoutCondition **(required)**
          - _(nesting depth limit — see `RouteReadTimeoutCondition` in the Schemas appendix)_
      - **`inactivityTimeout`**
        - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
          - _(nesting depth limit — see `InactivityTimeoutCondition` in the Schemas appendix)_
      - **`evaluation`**
        - `evaluation` — RouteEvaluationCondition **(required)**
          - _(nesting depth limit — see `RouteEvaluationCondition` in the Schemas appendix)_
- `task` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`sendMessage`**
      - `sendMessage` — RouteSendMessageTask **(required)**
        - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
        - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
    - **`sendGenerativeMessage`**
      - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
        - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
    - **`addMembers`**
      - `addMembers` — RouteAddMembersTask **(required)**
        - `emails` — array **(required)**
          - _array of_ `string`
    - **`notifyMessage`**
      - `notifyMessage` — RouteNotifyMessage **(required)**
        - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
        - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
        - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
        - `variables` — array — List of generative variables that can be used to customize the email message content.
          - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
    - **`notifyEmail`**
      - `notifyEmail` — RouteNotifyEmail **(required)**
        - `recipient` — string **(required)** — An email where to send the message.
        - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
        - `variables` — array — List of generative variables that can be used to customize the email message content.
          - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
- `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`RouteActionCondition`**

- _oneOf_ — exactly one of:
  - **`replyTimeout`**
    - `replyTimeout` — RouteReplyTimeoutCondition **(required)**
      - `timeout` — number **(required)** — The timeout in seconds during which the agent should not reply to the message in order to meet the condition. _(min=1; max=86400)_
  - **`readTimeout`**
    - `readTimeout` — RouteReadTimeoutCondition **(required)**
      - `timeout` — number **(required)** — Timeout in seconds during which the message should not be read by the agent to meet the condition. _(min=1; max=86400)_
  - **`inactivityTimeout`**
    - `inactivityTimeout` — InactivityTimeoutCondition **(required)**
      - `timeout` — number **(required)** — Timeout in seconds since last activity in the channel. _(min=1; max=86400)_
  - **`evaluation`**
    - `evaluation` — RouteEvaluationCondition **(required)**
      - `prompt` — string **(required)** — A natural language prompt used to evaluate the content of a customer's message using AI. The prompt should be formulated to guide the AI in determining whether the message or conversation meets a specific condition. _(minLen=1; maxLen=8000)_

**`RouteActionTask`**

- _oneOf_ — exactly one of:
  - **`sendMessage`**
    - `sendMessage` — RouteSendMessageTask **(required)**
      - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
      - `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_
  - **`sendGenerativeMessage`**
    - `sendGenerativeMessage` — RouteSendGenerativeMessageTask **(required)**
      - `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_
  - **`addMembers`**
    - `addMembers` — RouteAddMembersTask **(required)**
      - `emails` — array **(required)**
        - _array of_ `string`
  - **`notifyMessage`**
    - `notifyMessage` — RouteNotifyMessage **(required)**
      - `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
      - `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
      - `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
      - `variables` — array — List of generative variables that can be used to customize the email message content.
        - _array of_ `RouteGenerativeVariable`
          - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_
  - **`notifyEmail`**
    - `notifyEmail` — RouteNotifyEmail **(required)**
      - `recipient` — string **(required)** — An email where to send the message.
      - `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
      - `variables` — array — List of generative variables that can be used to customize the email message content.
        - _array of_ `RouteGenerativeVariable`
          - _(nesting depth limit — see `RouteGenerativeVariable` in the Schemas appendix)_

**`RouteAddMembersTask`**

- `emails` — array **(required)**
  - _array of_ `string`

**`RouteAgentTarget`**

- `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.

**`RouteBotTarget`**

- `id` — string **(required)** — An ID of the bot.

**`RouteEvaluationCondition`**

- `prompt` — string **(required)** — A natural language prompt used to evaluate the content of a customer's message using AI. The prompt should be formulated to guide the AI in determining whether the message or conversation meets a specific condition. _(minLen=1; maxLen=8000)_

**`RouteGenerativeVariable`**

- `term` — string **(required)** — Variable name, to be used in the message. Example: 'reason_of_complain'. _(pattern=^[a-zA-Z0-9_]+$)_
- `description` — string **(required)** — A description to guide AI when resolving the variable. _(minLen=1; maxLen=4000)_

**`RouteNotifyEmail`**

- `recipient` — string **(required)** — An email where to send the message.
- `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
- `variables` — array — List of generative variables that can be used to customize the email message content.
  - _array of_ `RouteGenerativeVariable`
    - `term` — string **(required)** — Variable name, to be used in the message. Example: 'reason_of_complain'. _(pattern=^[a-zA-Z0-9_]+$)_
    - `description` — string **(required)** — A description to guide AI when resolving the variable. _(minLen=1; maxLen=4000)_

**`RouteNotifyMessage`**

- `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
- `userId` — string — Identifier of the user who should receive the message. _(minLen=12; maxLen=12)_
- `channelId` — string — Identifier of the channel where message should be sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `text` — string **(required)** — Email content to be sent to the recipient. Can include variables for generative variables. _(minLen=1; maxLen=4000)_
- `variables` — array — List of generative variables that can be used to customize the email message content.
  - _array of_ `RouteGenerativeVariable`
    - `term` — string **(required)** — Variable name, to be used in the message. Example: 'reason_of_complain'. _(pattern=^[a-zA-Z0-9_]+$)_
    - `description` — string **(required)** — A description to guide AI when resolving the variable. _(minLen=1; maxLen=4000)_

**`RouteReadTimeoutCondition`**

- `timeout` — number **(required)** — Timeout in seconds during which the message should not be read by the agent to meet the condition. _(min=1; max=86400)_

**`RouteReplyTimeoutCondition`**

- `timeout` — number **(required)** — The timeout in seconds during which the agent should not reply to the message in order to meet the condition. _(min=1; max=86400)_

**`RouteRule`**

- _oneOf_ — exactly one of:
  - **`timeFrame`**
    - `timeFrame` — RouteTimeFrameRule **(required)**
      - `timeZone` — string **(required)** — The IANA time zone name (e.g., 'America/Los_Angeles') specifying the time zone in which the rule applies.
      - `day` — string **(required)** _(enum: `EVERY_DAY`, `WEEKDAYS`, `WEEKENDS`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`)_
      - `startMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_
      - `endMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_

**`RouteSendGenerativeMessageTask`**

- `botId` — string **(required)** — Identifier of the chatbot that should generate the message. _(minLen=12; maxLen=12)_

**`RouteSendMessageTask`**

- `botId` — string **(required)** — Identifier of the chatbot from whom the message will be sent. _(minLen=12; maxLen=12)_
- `text` — string **(required)** — Static message that should be sent to the user. _(minLen=1; maxLen=5000)_

**`RouteServiceTarget`**

- `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
- `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443

**`RouteTarget`**

- _oneOf_ — exactly one of:
  - **`service`**
    - `service` — RouteServiceTarget **(required)**
      - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
      - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
  - **`agent`**
    - `agent` — RouteAgentTarget **(required)**
      - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
  - **`bot`**
    - `bot` — RouteBotTarget **(required)**
      - `id` — string **(required)** — An ID of the bot.

**`RouteTimeFrameDay`**

- string _(enum: `EVERY_DAY`, `WEEKDAYS`, `WEEKENDS`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`)_

**`RouteTimeFrameRule`**

- `timeZone` — string **(required)** — The IANA time zone name (e.g., 'America/Los_Angeles') specifying the time zone in which the rule applies.
- `day` — string **(required)** _(enum: `EVERY_DAY`, `WEEKDAYS`, `WEEKENDS`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`)_
- `startMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_
- `endMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_

**`ScheduleCalendarEventRequestContent`**

- `channelId` — string — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `start` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])[tT ](2[0-4]|[01][0-9]):([0-5][0-9]):(60|[0-5][0-9])(\.\d+)?([zZ]|[+-]([0-5][0-9]):(60|[0-5][0-9]))$)_
- `duration` — string **(required)** _(pattern=^\d{4}-(?:0[0-9]{1}|1[0-2]{1})-(3[01]|0[1-9]|[12][0-9])$)_
- `attendees` — array
  - _array of_ `string`
- `summary` — string — Event title _(maxLen=255)_
- `language` — string
- `timeZone` — string

**`ScheduleCalendarEventResponseContent`**

- `channel` — Channel **(required)**
  - `subject` — string
  - `description` — string
  - `picture` — string — Picture URL
  - `pictureColor` — string — Picture dominant color represented by a hex value.
  - `access` — string _(enum: `private`, `public`)_
  - `company` — string
  - `context` — ChannelContext
    - `source` — string _(enum: `kite`)_
    - `target` — string
    - `events` — array
      - _array of_ `ChannelContextEvent`
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
    - `ptt` — ChannelContextPushToTalk
      - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
  - `kite` — boolean
  - `kiteTarget` — string
  - `kiteVariant` — string
  - `kiteAssign` — string
  - `kiteServiceName` — string
  - `kiteDefaultSubject` — string
  - `service` — string
  - `serviceTitle` — string
  - `serviceRecipient` — string
  - `assignee` — User
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
  - `telephony` — boolean
  - `sms` — boolean
  - `mms` — boolean
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
  - `messagingSenderId` — string
  - `messagingReplyUntil` — number
  - `broadcast` — boolean
  - `external` — boolean
  - `autoRecord` — boolean
  - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
  - `transcriptionLanguage` — string
  - `wizyGuestViewOnly` — boolean
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `channelType` — string **(required)** _(enum: `direct`, `group`)_
  - `memberCount` — number **(required)**
  - `createdAt` — string **(required)**
  - `createdBy` — string **(required)**
  - `updatedAt` — string
- `event` — CalendarEvent **(required)**
  - `id` — string
  - `owner` — string
  - `start` — string
  - `end` — string
  - `summary` — string
  - `attendees` — array
    - _array of_ `string`

**`Service`**

- `id` — number **(required)**
- `uri` — string **(required)**
- `title` — string **(required)**
- `settings` — ServiceSettings **(required)**
  - `phoneNumber` — string
  - `messagingNumber` — string
- `extensions` — array **(required)**
  - _array of_ `string`
- `pbx` — ServicePbx **(required)**
  - `domain` — string **(required)**
  - `port` — number **(required)**

**`ServicePbx`**

- `domain` — string **(required)**
- `port` — number **(required)**

**`ServiceSettings`**

- `phoneNumber` — string
- `messagingNumber` — string

**`SmsConfig`**

- `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `SmsConfigRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `RouteRule`
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `serviceNumber` — string **(required)**
- `createdAt` — string **(required)**
- `updatedAt` — string

**`SmsConfigRoute`**

- `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
- `rules` — array **(required)** _(minItems=1; maxItems=20)_
  - _array of_ `RouteRule`
    - _oneOf_ — exactly one of:
      - **`timeFrame`**
        - `timeFrame` — RouteTimeFrameRule **(required)**
          - _(nesting depth limit — see `RouteTimeFrameRule` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`SmsServiceNumber`**

- `number` — string **(required)** — A phone number registered though Classound.
- `service` — Service
  - `id` — number **(required)**
  - `uri` — string **(required)**
  - `title` — string **(required)**
  - `settings` — ServiceSettings **(required)**
    - `phoneNumber` — string
    - `messagingNumber` — string
  - `extensions` — array **(required)**
    - _array of_ `string`
  - `pbx` — ServicePbx **(required)**
    - `domain` — string **(required)**
    - `port` — number **(required)**

**`Template`**

- `name` — string **(required)**
- `parameterFormat` — string **(required)** _(enum: `NAMED`)_
- `components` — array **(required)**
  - _array of_ `Component`
    - `type` — string **(required)** _(enum: `HEADER`, `BODY`, `FOOTER`, `BUTTONS`)_
    - `format` — string **(required)** _(enum: `TEXT`, `IMAGE`, `DOCUMENT`, `VIDEO`)_
    - `text` — string
    - `example` — ComponentExample
      - `headerHandle` — array
        - _array of_ `string`
      - `bodyTextNamedParams` — array
        - _(nesting depth limit — see `BodyTextNamedParam` in the Schemas appendix)_
    - `buttons` — array
      - _array of_ `Button`
        - _(nesting depth limit — see `Button` in the Schemas appendix)_
- `language` — string **(required)**
- `status` — string **(required)** _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_
- `category` — string **(required)** _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_
- `subCategory` — string
- `id` — string **(required)**

**`TemplateCategory`**

- string _(enum: `MARKETING`, `UTILITY`, `AUTHENTICATION`)_

**`TemplateParameter`**

- `name` — string **(required)**
- `value` — string **(required)**

**`TemplateStatus`**

- string _(enum: `APPROVED`, `PAUSED`, `REJECTED`)_

**`TemplateWithParameters`**

- `name` — string **(required)**
- `parameters` — array
  - _array of_ `TemplateParameter`
    - `name` — string **(required)**
    - `value` — string **(required)**

**`UpdateWidgetRequestContent`**

- `appearance` — WidgetAppearance
  - `pallete` — WidgetPalleteSettings
    - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
  - `text` — WidgetTextSettings
    - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
    - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
    - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
    - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `WidgetRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `WidgetRouteRule`
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
  - _array of_ `WidgetWelcomeMessage`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `delay` — number — The time in milliseconds until the message will be visible to the end user.
- `name` — string **(required)** _(minLen=1; maxLen=100)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — WidgetServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — WidgetAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — WidgetBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
- `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
- `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
- `widgetRestrictions` — WidgetRestrictions
  - `anonymous` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `guest` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
- `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`UpdateWidgetResponseContent`**

- `widget` — Widget **(required)**
  - `appearance` — WidgetAppearance
    - `pallete` — WidgetPalleteSettings
      - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
      - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `text` — WidgetTextSettings
      - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
      - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
      - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
      - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
  - `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
    - _array of_ `WidgetRoute`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
      - `rules` — array **(required)** _(minItems=1; maxItems=20)_
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
      - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
      - `target` — union **(required)**
        - _(nesting depth limit — see `WidgetTarget` in the Schemas appendix)_
      - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
  - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
    - _array of_ `WidgetWelcomeMessage`
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `delay` — number — The time in milliseconds until the message will be visible to the end user.
  - `name` — string **(required)** _(minLen=1; maxLen=100)_
  - `target` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`service`**
        - `service` — WidgetServiceTarget **(required)**
          - _(nesting depth limit — see `WidgetServiceTarget` in the Schemas appendix)_
      - **`agent`**
        - `agent` — WidgetAgentTarget **(required)**
          - _(nesting depth limit — see `WidgetAgentTarget` in the Schemas appendix)_
      - **`bot`**
        - `bot` — WidgetBotTarget **(required)**
          - _(nesting depth limit — see `WidgetBotTarget` in the Schemas appendix)_
  - `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
  - `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
  - `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
  - `widgetRestrictions` — WidgetRestrictions
    - `anonymous` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
    - `guest` — WidgetRestrictionSet
      - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
      - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
      - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
      - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
      - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
      - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
  - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
    - _array of_ `RouteAction`
      - `id` — string **(required)** _(minLen=6; maxLen=6)_
      - `conditions` — array — List of conditions that must match before making an action.
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
      - `task` — union **(required)**
        - _(nesting depth limit — see `RouteActionTask` in the Schemas appendix)_
      - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
  - `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
  - `company` — string **(required)**
  - `createdAt` — string **(required)**
  - `updatedAt` — string

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

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WhatsAppConfig`**

- `serviceUri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443). The speicifed service is used during conversation creation which means that conversation can be linked to the same service as for phone calls.
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `WhatsAppConfigRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `RouteRule`
        - _(nesting depth limit — see `RouteRule` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- `companyId` — string **(required)** _(minLen=3; maxLen=30)_
- `serviceNumber` — string **(required)**
- `createdAt` — string **(required)**
- `updatedAt` — string

**`WhatsAppConfigRoute`**

- `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
- `rules` — array **(required)** _(minItems=1; maxItems=20)_
  - _array of_ `RouteRule`
    - _oneOf_ — exactly one of:
      - **`timeFrame`**
        - `timeFrame` — RouteTimeFrameRule **(required)**
          - _(nesting depth limit — see `RouteTimeFrameRule` in the Schemas appendix)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — RouteServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — RouteAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — RouteBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`WhatsAppServiceNumber`**

- `number` — string **(required)** — A WhatsApp phone number registered though Classound.
- `service` — Service
  - `id` — number **(required)**
  - `uri` — string **(required)**
  - `title` — string **(required)**
  - `settings` — ServiceSettings **(required)**
    - `phoneNumber` — string
    - `messagingNumber` — string
  - `extensions` — array **(required)**
    - _array of_ `string`
  - `pbx` — ServicePbx **(required)**
    - `domain` — string **(required)**
    - `port` — number **(required)**

**`Widget`**

- `appearance` — WidgetAppearance
  - `pallete` — WidgetPalleteSettings
    - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
    - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
  - `text` — WidgetTextSettings
    - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
    - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
    - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
    - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_
- `routes` — array — A list of routes that define different routing rules for the widget. Each route specifies a set of rules and a target to direct the interaction.
  - _array of_ `WidgetRoute`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
    - `rules` — array **(required)** _(minItems=1; maxItems=20)_
      - _array of_ `WidgetRouteRule`
        - _(nesting depth limit — see `WidgetRouteRule` in the Schemas appendix)_
    - `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
      - _array of_ `WidgetWelcomeMessage`
        - _(nesting depth limit — see `WidgetWelcomeMessage` in the Schemas appendix)_
    - `target` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`service`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`agent`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`bot`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
      - _array of_ `RouteAction`
        - _(nesting depth limit — see `RouteAction` in the Schemas appendix)_
- `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
  - _array of_ `WidgetWelcomeMessage`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `delay` — number — The time in milliseconds until the message will be visible to the end user.
- `name` — string **(required)** _(minLen=1; maxLen=100)_
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — WidgetServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — WidgetAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — WidgetBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `anonymousSessionsEnabled` — boolean — Controls whether unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed and the widget should be treated as authenticated-only.
- `anonymousSessionsOnly` — boolean — Controls whether only unauthenticated users are allowed to start guest sessions through this widget. If omitted, false is assumed. When enabled, anonymousSessionsEnabled is treated as enabled as well, login methods should be hidden, and the widget should start the anonymous flow directly.
- `anonymousSessionsRandomNameEnabled` — boolean — Controls whether anonymous visitors should receive generated display names instead of entering names manually. Applies only when anonymous sessions are allowed. If omitted, false is assumed.
- `widgetRestrictions` — WidgetRestrictions
  - `anonymous` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
  - `guest` — WidgetRestrictionSet
    - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
    - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
    - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
    - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
    - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
    - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
- `skipWelcomeScreen` — boolean — When enabled, the widget skips the welcome screen and opens the chat immediately. An existing conversation for this widget is reused; otherwise a new one is started. If omitted, false is assumed and the welcome screen is shown.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.
- `id` — string **(required)** _(pattern=^[0-9a-z]{8}$)_
- `company` — string **(required)**
- `createdAt` — string **(required)**
- `updatedAt` — string

**`WidgetAgentTarget`**

- `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.

**`WidgetAppearance`**

- `pallete` — WidgetPalleteSettings
  - `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
  - `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
- `text` — WidgetTextSettings
  - `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
  - `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
  - `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
  - `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_

**`WidgetBotTarget`**

- `id` — string **(required)** — An ID of the bot.

**`WidgetPalleteSettings`**

- `backgroundColor` — string — The background color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_
- `accentColor` — string — The accent color can be specified in hex format (#CCC or #FAFAFA), rgb format (rgb(22, 123, 200)), or rgba format (rgba(22, 123, 200, 1)). _(pattern=^(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b|rgb\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*\)|rgba\(\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*,\s*(0|1|0?\.\d+)\s*\)$)_

**`WidgetRestrictionSet`**

- `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
- `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
- `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
- `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
- `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
- `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.

**`WidgetRestrictions`**

- `anonymous` — WidgetRestrictionSet
  - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
  - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
  - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
  - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
  - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
  - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.
- `guest` — WidgetRestrictionSet
  - `addMembersDisabled` — boolean — Hide the 'Add member' button and reject add-member API calls for this audience. If omitted, false is assumed.
  - `startConferenceDisabled` — boolean — Hide the 'Start/Join conference' button and reject conference creation for this audience. If omitted, false is assumed.
  - `attachFilesDisabled` — boolean — Hide the attachment picker and reject attachment uploads for this audience. If omitted, false is assumed.
  - `exportConversationDisabled` — boolean — Hide the 'Export conversation' action for this audience. If omitted, false is assumed.
  - `notificationsSettingsDisabled` — boolean — Hide the widget settings (gear) button and disable notifications for this audience. If omitted, false is assumed.
  - `installAppBannerDisabled` — boolean — Hide the install app banner in the widget conversation for this audience. If omitted, false is assumed.

**`WidgetRoute`**

- `id` — string **(required)** _(pattern=^[0-9a-z]{4}$)_
- `rules` — array **(required)** _(minItems=1; maxItems=20)_
  - _array of_ `WidgetRouteRule`
    - _oneOf_ — exactly one of:
      - **`timeFrame`**
        - `timeFrame` — WidgetRouteTimeFrameRule **(required)**
          - _(nesting depth limit — see `WidgetRouteTimeFrameRule` in the Schemas appendix)_
- `welcomeMessages` — array — A list of welcome messages that will be sent to the user when they first interact with the widget. _(minItems=1; maxItems=10)_
  - _array of_ `WidgetWelcomeMessage`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `delay` — number — The time in milliseconds until the message will be visible to the end user.
- `target` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`service`**
      - `service` — WidgetServiceTarget **(required)**
        - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
        - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
    - **`agent`**
      - `agent` — WidgetAgentTarget **(required)**
        - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
    - **`bot`**
      - `bot` — WidgetBotTarget **(required)**
        - `id` — string **(required)** — An ID of the bot.
- `actions` — array — Actions that will be used if the specified route and the conditions within a specific action are met.
  - _array of_ `RouteAction`
    - `id` — string **(required)** _(minLen=6; maxLen=6)_
    - `conditions` — array — List of conditions that must match before making an action.
      - _array of_ `RouteActionCondition`
        - _(nesting depth limit — see `RouteActionCondition` in the Schemas appendix)_
    - `task` — union **(required)**
      - _oneOf_ — exactly one of:
        - **`sendMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`sendGenerativeMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`addMembers`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyMessage`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
        - **`notifyEmail`**
          - _(nesting depth limit — inline object, see the parent schema in the Schemas appendix)_
    - `once` — boolean — Indicates whether the action should be run only once, regardless of how many times the conditions are met.

**`WidgetRouteRule`**

- _oneOf_ — exactly one of:
  - **`timeFrame`**
    - `timeFrame` — WidgetRouteTimeFrameRule **(required)**
      - `timeZone` — string **(required)** — The IANA time zone name (e.g., 'America/Los_Angeles') specifying the time zone in which the rule applies.
      - `day` — string **(required)** _(enum: `EVERY_DAY`, `WEEKDAYS`, `WEEKENDS`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`)_
      - `startMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_
      - `endMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_

**`WidgetRouteTimeFrameRule`**

- `timeZone` — string **(required)** — The IANA time zone name (e.g., 'America/Los_Angeles') specifying the time zone in which the rule applies.
- `day` — string **(required)** _(enum: `EVERY_DAY`, `WEEKDAYS`, `WEEKENDS`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`)_
- `startMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_
- `endMinute` — number **(required)** — The minute of the day when the rule matches for the specified time zone (for example, 300 corresponds to 5AM) _(min=1; max=1440)_

**`WidgetServiceTarget`**

- `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
- `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443

**`WidgetTarget`**

- _oneOf_ — exactly one of:
  - **`service`**
    - `service` — WidgetServiceTarget **(required)**
      - `id` — number **(required)** — An ID of the service. ID of the service equals the ID of the call group that available on the PBX.
      - `uri` — string **(required)** — An URI of the service which includes ID, PBX domain and port (example - 1@example.wildixin.com:443
  - **`agent`**
    - `agent` — WidgetAgentTarget **(required)**
      - `email` — string **(required)** — An email of the user that registered on x-bees and account must be connected to the PBX.
  - **`bot`**
    - `bot` — WidgetBotTarget **(required)**
      - `id` — string **(required)** — An ID of the bot.

**`WidgetTextSettings`**

- `button` — string — Text that will be visible to the user inside Send button (default: Start new conversation) _(minLen=1)_
- `title` — string — Text that will be visible to the user below avatar (default: Support agent) _(minLen=1)_
- `topTitle` — string — Text that will be visible to the user in the header title (default: Hello) _(minLen=1)_
- `topSubtitle` — string — Text that will be visible to the user in the header subtitle (default: How can we help you?) _(minLen=1)_

**`WidgetWelcomeMessage`**

- `text` — string _(minLen=1; maxLen=5000)_
- `elements` — array
  - _array of_ `Element`
    - _oneOf_ — exactly one of:
      - **`template`**
        - `template` — MessageTemplateConfig **(required)**
          - _(nesting depth limit — see `MessageTemplateConfig` in the Schemas appendix)_
      - **`actions`**
        - `actions` — array **(required)**
          - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
      - **`wilma`**
        - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
          - _(nesting depth limit — see `WilmaChatElement` in the Schemas appendix)_
- `delay` — number — The time in milliseconds until the message will be visible to the end user.

**`WilmaChatArtifact`**

_An artifact the turn shared. The files stay in the artifacts store; `artifactId` opens it._

- `artifactId` — string **(required)** _(minLen=1; maxLen=64)_
- `title` — string **(required)** _(minLen=1; maxLen=256)_
- `kind` — string **(required)** _(minLen=1; maxLen=32)_
- `size` — number **(required)** _(min=0)_
- `name` — string _(minLen=1; maxLen=256)_

**`WilmaChatElement`**

_On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex)._

- `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
- `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
- `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
- `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
- `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
- `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
  - `outcome` — string **(required)** — How the turn ended. _(enum: `done`, `stopped`, `failed`)_
  - `durationMs` — number — From the turn's start to its end. Absent when the turn had not ended.
  - `toolCount` — number **(required)** — Steps the turn took, counted as the Wilma assistant counts its work steps: each tool call and each sandbox step (`SandboxStartedEvent`, `SandboxFailedEvent`).
  - `failedCount` — number **(required)** — Steps that failed: calls that failed, including those the stop or failure cut off, and sandbox steps that failed.
- `artifacts` — array
  - _array of_ `WilmaChatArtifact`
    - `artifactId` — string **(required)** _(minLen=1; maxLen=64)_
    - `title` — string **(required)** _(minLen=1; maxLen=256)_
    - `kind` — string **(required)** _(minLen=1; maxLen=32)_
    - `size` — number **(required)** _(min=0)_
    - `name` — string _(minLen=1; maxLen=256)_

**`WilmaChatTurnOutcome`**

_How the turn ended._

- string _(enum: `done`, `stopped`, `failed`)_

**`WilmaChatTurnSummary`**

_How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log._

- `outcome` — string **(required)** — How the turn ended. _(enum: `done`, `stopped`, `failed`)_
- `durationMs` — number — From the turn's start to its end. Absent when the turn had not ended.
- `toolCount` — number **(required)** — Steps the turn took, counted as the Wilma assistant counts its work steps: each tool call and each sandbox step (`SandboxStartedEvent`, `SandboxFailedEvent`).
- `failedCount` — number **(required)** — Steps that failed: calls that failed, including those the stop or failure cut off, and sandbox steps that failed.

</details>
