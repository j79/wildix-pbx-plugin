## Conversations API

_OpenAPI: x-bees conversations service — version v2_

**Servers**

- `https://api.x-bees.com` — Production
- `https://api-stable.x-bees.com` — Stable
- `https://api-stage.x-bees.com` — Stage

### Channels

#### `GET` `/v2/conversations/channels/`

Lists all channels associated with a user. Allows pagination using limit and offset parameters. Sorted by last message in the channel.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ListChannels`
- **Scopes**: `messaging:ListChannels`, `messaging:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The unique identifier of the user when a service or PBX token is used. _(minLen=12; maxLen=12)_
  - `limit` (query) — number — The maximum number of channels to return. The value must be between 1 and 30. _(min=1; max=30)_
  - `offset` (query) — number — The offset from which to start listing channels. The value must be between 0 and 1000. _(min=0; max=1000)_
- **Response 200** (`ListChannelsResponseContent`)
  - `channels` — array **(required)** — A list of channels associated with the user.
    - _array of_ `Channel`
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
- Errors: `400`, `403`, `429`

#### `GET` `/v2/conversations/channels/{channelId}`

Retrieves details of a specific channel by its unique identifier.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetChannel`
- **Scopes**: `messaging:GetChannel`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- **Response 200** (`GetChannelResponseContent`)
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
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/conversations/channels/{channelId}`

Updates the details of an existing channel. This operation can modify channel properties such as name, description, and members.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `UpdateChannel`
- **Scopes**: `messaging:UpdateChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to be updated. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UpdateChannelRequestContent`)
  - `subject` — string — The subject of the channel. _(minLen=1; maxLen=80)_
  - `description` — string — The description of the channel. _(maxLen=160)_
  - `picture` — string — The URL of the channel's picture. _(pattern=^https://[^\s/$.?#].[^\s]*$)_
  - `pictureColor` — string — The dominant color of the channel's picture, represented by a hex value. _(pattern=^#[0-9a-fA-F]{6}$)_
  - `access` — string _(enum: `private`, `public`)_
  - `broadcast` — boolean — Indicates if the channel is broadcast-only. Default is false.
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
            - `email` — string **(required)**
            - `name` — string
            - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
    - `ptt` — ChannelContextPushToTalk
      - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
  - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
  - `sms` — boolean — Indicates if the channel supports SMS. Default is false.
  - `mms` — boolean — Indicates if the channel supports MMS. Default is false.
  - `whatsapp` — boolean — Indicates if the channel supports WhatsApp. Default is false.
  - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
  - `messagingSenderId` — string — The business side of the conversation: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. A reply has to name the sender it is sent from. On Messenger and Instagram kite writes it from the inbound event, because the channel id hashes the sender's linked service and not the sender; on RCS the channel id includes the brand, and it is written when the channel is created.
  - `messagingReplyUntil` — number — Epoch seconds until which a reply still reaches the person. On Messenger and Instagram this is Meta's 7 day HUMAN_AGENT deadline, restarted by each inbound message; classound applies the tag itself, so this is the one deadline a client has to show. 0 means the deadline is not known, which is what the inbound event carries when the session row was gone before it could be read back; it does not mean the window has closed, so a client reads the window as closed on `messagingReplyUntil > 0 && now > messagingReplyUntil` and shows nothing at 0. Absent on a channel with no reply window.
  - `kiteAssign` — string — The unique identifier of the assignee.
  - `serviceTitle` — string
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
  - `autoRecord` — boolean
  - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
  - `transcriptionLanguage` — string
  - `wizyGuestViewOnly` — boolean
  - `silent` — boolean — Set to true to suppress system messages about the updates. Default is false.
- **Response 200** (`UpdateChannelResponseContent`)
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
- Errors: `400`, `403`, `404`, `429`

#### `PATCH` `/v2/conversations/channels/{channelId}`

Partially updates the details of an existing channel. This operation allows for updating specific channel properties without altering the entire resource.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `PartialUpdateChannel`
- **Scopes**: `messaging:PartialUpdateChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to be updated. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `PartialUpdateChannelRequestContent`)
  - `silent` — boolean — Set to true to suppress system messages about the updates. Default is false.
  - `set` — PartialUpdateChannelSetOptions
    - `subject` — string — The subject of the channel. _(minLen=1; maxLen=80)_
    - `description` — string — The description of the channel. _(maxLen=160)_
    - `picture` — string — The URL of the channel's picture. _(pattern=^https://[^\s/$.?#].[^\s]*$)_
    - `pictureColor` — string — The dominant color of the channel's picture, represented by a hex value. _(pattern=^#[0-9a-fA-F]{6}$)_
    - `access` — string _(enum: `private`, `public`)_
    - `broadcast` — boolean — Indicates if the channel is broadcast-only. Default is false.
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
    - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
    - `sms` — boolean — Indicates if the channel supports SMS. Default is false.
    - `mms` — boolean — Indicates if the channel supports MMS. Default is false.
    - `whatsapp` — boolean — Indicates if the channel supports WhatsApp. Default is false.
    - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
    - `messagingSenderId` — string — The business side of the conversation: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. A reply has to name the sender it is sent from. On Messenger and Instagram kite writes it from the inbound event, because the channel id hashes the sender's linked service and not the sender; on RCS the channel id includes the brand, and it is written when the channel is created.
    - `messagingReplyUntil` — number — Epoch seconds until which a reply still reaches the person. On Messenger and Instagram this is Meta's 7 day HUMAN_AGENT deadline, restarted by each inbound message; classound applies the tag itself, so this is the one deadline a client has to show. 0 means the deadline is not known, which is what the inbound event carries when the session row was gone before it could be read back; it does not mean the window has closed, so a client reads the window as closed on `messagingReplyUntil > 0 && now > messagingReplyUntil` and shows nothing at 0. Absent on a channel with no reply window.
    - `kiteAssign` — string — The unique identifier of the assignee.
    - `serviceTitle` — string
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
    - `autoRecord` — boolean
    - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
    - `transcriptionLanguage` — string
    - `wizyGuestViewOnly` — boolean
  - `unset` — array — Options to unset specific fields in the channel.
    - _array of_ `GroupChannelUnsetOptions`
- **Response 200** (`PartialUpdateChannelResponseContent`)
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
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/conversations/channels/{channelId}`

Deletes an existing channel. This operation is idempotent, meaning that if the channel does not exist, the operation will still return a successful response.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `DeleteChannel`
- **Scopes**: `messaging:DeleteChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to be deleted. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/assign`

Assigns a channel to a user and/or service, optionally managing members according to a variant.

- operationId: `AssignChannel`
- **Scopes**: `messaging:AssignChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `AssignChannelRequestContent`)
  - `silent` — boolean — True to not send a system message that channel was assigned to specific service or user. Default - false.
  - `service` — union
    - _oneOf_ — exactly one of:
      - **`uri`**
        - `uri` — string **(required)** — A unique identifier of the service. URI structure - <serviceId>@<pbxDomain>:<pbxPort> (example 1@demo.wildix.com:433) _(pattern=^\d+@.+:\d+$)_
  - `assignee` — union
    - _oneOf_ — exactly one of:
      - **`id`**
        - `id` — string **(required)** — A User ID of the assignee.
      - **`email`**
        - `email` — string **(required)** — An email of the assignee.
  - `variant` — string _(enum: `ADAPTIVE`, `SELECTED`, `EVERYBODY`, `SKIP`)_
- **Response 200** (`AssignChannelResponseContent`)
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

#### `POST` `/v2/conversations/channels/{channelId}/hide`

Allows a user to hide an existing channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `HideChannel`
- **Scopes**: `messaging:HideChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to hide. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/join`

Allows a user to join an existing channel. This operation requires the channel to be accessible to the user. The user can join a channel if it is public or if they have the necessary permissions.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 60 | 50 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `JoinChannel`
- **Scopes**: `messaging:JoinChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to join. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `JoinChannelRequestContent`)
  - `silent` — boolean — Set to true to suppress system messages that the user joined the channel. Default is false.
- **Response 200** (`JoinChannelResponseContent`)
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
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/leave`

Allows a user to leave an existing channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `LeaveChannel`
- **Scopes**: `messaging:LeaveChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to leave. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `LeaveChannelRequestContent`)
  - `silent` — boolean — Set to true to suppress system messages that the user left the channel. Default is false.
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/pin`

Marks the channel with a pin flag.
  A user can have up to 10 pinned channels. If a user tries to pin more than 10 channels, the system will remove the oldest channel if the force flag is specified; otherwise, a PinnedChannelsLimitReachedException will be thrown.
  The system will automatically remove the channel from pinned list if the user leaves the channel or if the channel is removed.
  This operation is idempotent, meaning that if the channel is already pinned, no error will be thrown.

- operationId: `PinChannel`
- **Scopes**: `messaging:PinChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel which should be pinned. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
  - `force` (query) — boolean — A flag that indicates whether the system should replace the oldest pinned channel with a new one if the limit of pinned channels is reached. If the force option is specified as false and the user already has the maximum limit of pinned channels, then the system will respond with an error.
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/conversations/channels/{channelId}/pin`

Removes pin flag from the the channel.

- operationId: `UnpinChannel`
- **Scopes**: `messaging:UnpinChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel which should be unpinned. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/read`

Marks all messages in the specified channel as read by the user. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 60 | 50 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `MarkRead`
- **Scopes**: `messaging:MarkRead`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel whose messages are to be marked as read. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/show`

Allows a user to show an existing hidden channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ShowChannel`
- **Scopes**: `messaging:ShowChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to show. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/conversations/channels/{channelId}/tags/{tagId}`

Marks the channel with specified tag.
  A user can have up to 100 channels tagged for a single tag. If a user tries to tag more than 100 channels, the system will remove the oldest channel tagged if the force flag is specified; otherwise, a TaggedChannelsLimitReachedException will be thrown.
  The system will automatically remove the channel from the specified tag if the user leaves the channel or if the channel is removed.
  This operation is idempotent, meaning that if the channel is already tagged, no error will be thrown.

- operationId: `TagChannel`
- **Scopes**: `messaging:TagChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel whose messages are to be marked as unread. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `tagId` (path) — string **(required)** — The unique identifier of the tag to add to the channel. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
  - `force` (query) — boolean — A flag that indicates whether the system should replace the oldest tagged channel with a new one if the limit of tagged channels is reached. If the force option is specified as false and the user already has the maximum limit of tagged channels for the tag, then the system will respond with an error.
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/conversations/channels/{channelId}/unread`

Marks the channel with unread indicator.
  A user can have up to 100 channels marked as unread. If a user tries to tag more than 100 channels, the system will remove the oldest channel unread marked if the force flag is specified; otherwise, a MarkUnreadChannelsLimitReachedException will be thrown.
  The system will automatically remove the unread mark from the channel if the user reads the messages using the MarkRead operation.
  This operation is idempotent, meaning that if the channel is already marked as unread, no error will be thrown.


**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 60 | 50 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `MarkUnread`
- **Scopes**: `messaging:MarkUnread`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel whose messages are to be marked as unread. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
  - `force` (query) — boolean — A flag that indicates whether the system should replace the oldest marked unread channel with a new one if the limit of unread marked channels is reached. If the force option is specified as false and the user already has the maximum limit of unread marked channels, then the system will respond with an error.
- **Request body** (`application/json` — `MarkUnreadRequestContent`)
  - `messageId` — string — A Message ID in the channel from which to calculate the amount of unread messages. _(minLen=32; maxLen=32)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/untag`

Removes specified tag from the the channel.

- operationId: `UntagChannel`
- **Scopes**: `messaging:UntagChannel`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel whose messages are to be marked as unread. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UntagChannelRequestContent`) **(required)**
  - `tagId` — string **(required)** — The unique identifier of the tag to remove from the channel. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/direct/get_channel_id`

Gets the channel ID of an existing or non-existing direct channel between the specified user and another member.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetDirectChannelId`
- **Scopes**: `messaging:GetDirectChannelId`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetDirectChannelIdRequestContent`)
  - `memberId` — string — A User ID of the member to connect with the direct channel. _(minLen=12; maxLen=12)_
  - `memberToInvite` — UserToInvite
    - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
    - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
- **Response 200** (`GetDirectChannelIdResponseContent`)
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/direct/get_or_create_channel`

Gets or creates a direct channel between the specified user and another member.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetOrCreateDirectChannel`
- **Scopes**: `messaging:GetOrCreateDirectChannel`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetOrCreateDirectChannelRequestContent`)
  - `memberId` — string — A User ID of the member to connect with the direct channel. _(minLen=12; maxLen=12)_
  - `memberToInvite` — UserToInvite
    - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
    - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
- **Response 200** (`GetOrCreateDirectChannelResponseContent`)
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
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/group`

Creates a new group channel with specified members and members to invite.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `CreateGroupChannel`
- **Scopes**: `messaging:CreateGroupChannel`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `CreateGroupChannelRequestContent`)
  - `subject` — string — The subject of the channel. _(minLen=1; maxLen=80)_
  - `description` — string — The description of the channel. _(maxLen=160)_
  - `picture` — string — The URL of the channel's picture. _(pattern=^https://[^\s/$.?#].[^\s]*$)_
  - `pictureColor` — string — The dominant color of the channel's picture, represented by a hex value. _(pattern=^#[0-9a-fA-F]{6}$)_
  - `access` — string _(enum: `private`, `public`)_
  - `broadcast` — boolean — Indicates if the channel is broadcast-only. Default is false.
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
            - `email` — string **(required)**
            - `name` — string
            - `status` — string **(required)** _(enum: `accepted`, `tentative`, `declined`, `none`)_
    - `ptt` — ChannelContextPushToTalk
      - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
  - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
  - `sms` — boolean — Indicates if the channel supports SMS. Default is false.
  - `mms` — boolean — Indicates if the channel supports MMS. Default is false.
  - `whatsapp` — boolean — Indicates if the channel supports WhatsApp. Default is false.
  - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
  - `messagingSenderId` — string — The business side of the conversation: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. A reply has to name the sender it is sent from. On Messenger and Instagram kite writes it from the inbound event, because the channel id hashes the sender's linked service and not the sender; on RCS the channel id includes the brand, and it is written when the channel is created.
  - `messagingReplyUntil` — number — Epoch seconds until which a reply still reaches the person. On Messenger and Instagram this is Meta's 7 day HUMAN_AGENT deadline, restarted by each inbound message; classound applies the tag itself, so this is the one deadline a client has to show. 0 means the deadline is not known, which is what the inbound event carries when the session row was gone before it could be read back; it does not mean the window has closed, so a client reads the window as closed on `messagingReplyUntil > 0 && now > messagingReplyUntil` and shows nothing at 0. Absent on a channel with no reply window.
  - `kiteAssign` — string — The unique identifier of the assignee.
  - `serviceTitle` — string
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
  - `autoRecord` — boolean
  - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
  - `transcriptionLanguage` — string
  - `wizyGuestViewOnly` — boolean
  - `channelId` — string — The unique identifier for the new group channel. If not provided, the system will generate one. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `members` — array — A list of user IDs to be added as members of the group channel.
    - _array of_ `string`
  - `membersToInvite` — array — A list of users to invite to the group channel, identified by their email addresses or phone numbers.
    - _array of_ `UserToInvite`
      - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
      - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
      - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
  - `creationEventType` — string — Defines which system event is emitted when a group channel is created. _(enum: `conversation_created`, `conversation_created_with_name`)_
- **Response 200** (`CreateGroupChannelResponseContent`)
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
- Errors: `400`, `401`, `403`, `429`

#### `POST` `/v2/conversations/kite`

Creates a new kite channel with specified widget or email.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 60 | 20 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `CreateKiteChannel`
- **Scopes**: `messaging:CreateKiteChannel`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `CreateKiteChannelRequestContent`) **(required)**
  - `channelId` — string — The unique identifier for the new group channel. If not provided, the system will generate one. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `targetId` — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or vadim.ruban@wildix.com).
  - `targetRouteId` — string — The unique identifier of the route for time-based configuration.
  - `welcomeMessages` — array — A list of welcome messages is created during channel creation to preserve the same state as the client has on the interface. If welcomeMessages or initialMessage are not specified, the system will generate a 'conversation was created' system message.
    - _array of_ `WelcomeMessage`
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
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `quote` — MessageQuote
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `text` — string _(minLen=1; maxLen=5000)_
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `mentions` — array
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
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `createdAt` — string **(required)**
        - `updatedAt` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `messageId` — string **(required)** — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
      - `mentions` — array — A list of user IDs mentioned in the message.
        - _array of_ `string`
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
  - `initialMessage` — InitialMessage
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `messageId` — string **(required)** — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
    - `mentions` — array — A list of user IDs mentioned in the message.
      - _array of_ `string`
- **Response 200** (`CreateKiteChannelResponseContent`)
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
- Errors: `400`, `401`, `403`, `404`, `429`

#### `POST` `/v2/conversations/messaging/get_channel_id`

Gets the channel ID of an existing or non-existing channel on a customer messaging channel (see MessagingChannel). The person is named by recipientId, the x-bees user invited for them; recipientNumber names the same person directly. Either value resolves to the channel's own customer id: the Page Scoped ID on Messenger, an opaque supplier identifier and not a phone number, and the phone number on RCS.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetMessagingChannelId`
- **Scopes**: `messaging:GetMessagingChannelId`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetMessagingChannelIdRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
  - `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `senderId` — string — The business sender the conversation runs from: the brand id on RCS, where it is required and is part of the channel id, so two brands never share a conversation with one person. Messenger and Instagram do not read it. The grammar classound and kite enforce for a brand id. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
- **Response 200** (`GetMessagingChannelIdResponseContent`)
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/messaging/get_or_create_channel`

Gets or creates a channel on a customer messaging channel (see MessagingChannel). The person is named by recipientId, the x-bees user invited for them; recipientNumber names the same person directly. Either value resolves to the channel's own customer id: the Page Scoped ID on Messenger, an opaque supplier identifier and not a phone number, and the phone number on RCS. The channel id carries the channel, so the same person on two channels, or a number that also has an SMS or WhatsApp chat, gets two conversations.

- operationId: `GetOrCreateMessagingChannel`
- **Scopes**: `messaging:GetOrCreateMessagingChannel`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetOrCreateMessagingChannelRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
  - `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `senderId` — string — The business sender the conversation runs from: the brand id on RCS, where it is required and is part of the channel id, so two brands never share a conversation with one person. Messenger and Instagram do not read it. The grammar classound and kite enforce for a brand id. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
  - `outgoing` — boolean — Indicates if the channel is outgoing. It's prevents applying routing settings for the channel. This parameter will be reset to false after 48 hours. Default is false.
- **Response 200** (`GetOrCreateMessagingChannelResponseContent`)
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
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/query-channels`

Query channels matched specified query. Allows pagination using limit and offset parameters. Sorted by last message in the channel.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `QueryChannels`
- **Scopes**: `messaging:QueryChannels`, `messaging:read`
- **Parameters**
  - `company` (query) — string — The unique identifier of the tenant when a service token is used. _(minLen=3; maxLen=30)_
  - `user` (query) — string — The unique identifier of the user when a service or PBX token is used. _(minLen=12; maxLen=12)_
  - `limit` (query) — number — The maximum number of channels to return. The value must be between 1 and 30. _(min=1; max=30)_
  - `offset` (query) — number — The offset from which to start listing channels. The value must be between 0 and 1000. _(min=0; max=1000)_
- **Request body** (`application/json` — `QueryChannelsRequestContent`)
  - `query` — ChannelsQuery
    - `ids` — array _(maxItems=30)_
      - _array of_ `string`
- **Response 200** (`QueryChannelsResponseContent`)
  - `channels` — array **(required)** — A list of channels matched the query.
    - _array of_ `Channel`
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
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/sms/get_channel_id`

Gets the channel ID of an existing or non-existing SMS channel

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetSmsChannelId`
- **Scopes**: `messaging:GetSmsChannelId`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetSmsChannelIdRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- **Response 200** (`GetSmsChannelIdResponseContent`)
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/sms/get_or_create_channel`

Gets or creates a SMS channel

- operationId: `GetOrCreateSmsChannel`
- **Scopes**: `messaging:GetOrCreateSmsChannel`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetOrCreateSmsChannelRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
  - `outgoing` — boolean — Indicates if the channel is outgoing. It's prevents applying routing settings for the channel. This parameter will be reset to false after 48 hours. Default is false.
- **Response 200** (`GetOrCreateSmsChannelResponseContent`)
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
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/telephony/get_channel_id`

Gets the channel ID of an existing or non-existing telephony channel

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetTelephonyChannelId`
- **Scopes**: `messaging:GetTelephonyChannelId`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetTelephonyChannelIdRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- **Response 200** (`GetTelephonyChannelIdResponseContent`)
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/telephony/get_or_create_channel`

Gets or creates a telephony channel

- operationId: `GetOrCreateTelephonyChannel`
- **Scopes**: `messaging:GetOrCreateTelephonyChannel`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetOrCreateTelephonyChannelRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- **Response 200** (`GetOrCreateTelephonyChannelResponseContent`)
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
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/whatsapp/get_channel_id`

Gets the channel ID of an existing or non-existing WhatsApp

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetWhatsAppChannelId`
- **Scopes**: `messaging:GetWhatsAppChannelId`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetWhatsAppChannelIdRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- **Response 200** (`GetWhatsAppChannelIdResponseContent`)
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/whatsapp/get_or_create_channel`

Gets or creates a WhatsApp channel

- operationId: `GetOrCreateWhatsAppChannel`
- **Scopes**: `messaging:GetOrCreateWhatsAppChannel`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. Required if used PBX or S2S token. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `GetOrCreateWhatsAppChannelRequestContent`) **(required)**
  - `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
  - `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
  - `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
  - `outgoing` — boolean — Indicates if the channel is outgoing. It's prevents applying routing settings for the channel. This parameter will be reset to false after 48 hours. Default is false.
- **Response 200** (`GetOrCreateWhatsAppChannelResponseContent`)
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
- Errors: `400`, `403`, `429`

### Files

#### `POST` `/v2/conversations/channels/{channelId}/files`

Create a presigned URL for file upload in the channel.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 60 | 20 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `UploadFile`
- **Scopes**: `messaging:UploadFile`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel.
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UploadFileRequestContent`) **(required)**
  - `name` — string **(required)** — The name of the file. Unreadable characters will be replaced with underscores. _(minLen=1; maxLen=255)_
  - `options` — UploadFileOptions
    - `category` — string _(enum: `channels`, `recordings`, `wizyconfRecordings`)_
    - `region` — string — The region in which you need to upload the file. It is only for s2s, in other cases it will be ignored.
- **Response 200** (`UploadFileResponseContent`)
  - `fileId` — string **(required)** — The unique identifier of the file.
  - `presignedUploadUrl` — string **(required)** — The presigned URL for uploading the file.
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/channels/{channelId}/files/{fileId}`

Retrieves information about an uploaded file in a specified channel.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 100 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 60 | 100 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 60 | 300 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 300 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetUploadedFileInfo`
- **Scopes**: `messaging:GetUploadedFileInfo`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the file.
  - `fileId` (path) — string **(required)** — The unique identifier of the file.
  - `category` (query) — string — The category of the file, either channel files or conference recordings. Default: channels. _(enum: `channels`, `recordings`, `wizyconfRecordings`)_
- **Response 200** (`GetUploadedFileInfoResponseContent`)
  - `file` — MessageAttachment **(required)**
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/channels/{channelId}/messages/{messageId}/files/{fileId}/download_url`

Retrieves a presigned URL for downloading a specific file from a message in a specified channel.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 60 | 50 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetFilePresignedDownloadUrl`
- **Scopes**: `messaging:GetFilePresignedDownloadUrl`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message.
  - `messageId` (path) — string **(required)** — The unique identifier of the message containing the file.
  - `fileId` (path) — string **(required)** — The unique identifier of the file to download.
  - `category` (query) — string — The category of the file, either channel files or conference recordings. _(enum: `channels`, `recordings`, `wizyconfRecordings`)_
  - `download` (query) — number — URL behavior, 0 - open(play) for audio/video, others are downloaded; 1 — always download. _(default=0)_
- **Response 200** (`GetFilePresignedDownloadUrlResponseContent`)
  - `presignedDownloadUrl` — string **(required)** — The presigned URL for downloading the file.
- Errors: `400`, `403`, `404`, `429`

### Members

#### `GET` `/v2/conversations/channels/{channelId}/members`

Retrieves a list of members for a specific channel. Supports pagination through limit and offset parameters.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 100 |
| XBS | 3600 | 600 |
| PBX | 60 | 300 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 300 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ListChannelMembers`
- **Scopes**: `messaging:ListChannelMembers`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel whose members are to be listed. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `limit` (query) — number — The maximum number of members to return. The value must be between 1 and 100. _(min=1; max=100)_
  - `offset` (query) — number — The offset from which to start listing members. The value must be between 0 and 1000. _(min=0; max=1000)_
- **Response 200** (`ListChannelMembersResponseContent`)
  - `members` — array **(required)** — The list of members matching the query.
    - _array of_ `ChannelMember`
      - `id` — string **(required)**
      - `createdAt` — string **(required)**
      - `role` — string **(required)** _(enum: `member`, `supervisor`)_
  - `users` — array **(required)** — The list of users matching the query
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

#### `POST` `/v2/conversations/channels/{channelId}/members`

Adds a single member to an existing channel.
This operation will either add an existing user or invite a new user to the channel.
This operation is idempotent, meaning that if the member already exists, the operation will still return a successful response.
If the specified member cannot be added because the account is deactivated in GetStream, the operation fails with `MemberDeactivatedException`.


**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `AddChannelMember`
- **Scopes**: `messaging:AddChannelMember`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which the member is to be added. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `AddChannelMemberRequestContent`)
  - `silent` — boolean — True to not send a system message that members added from the conversartion. Default - false.
  - `memberId` — string — A User ID of the member to be added to the channel. _(minLen=12; maxLen=12)_
  - `memberToInvite` — UserToInvite
    - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
    - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
  - `hideHistory` — boolean — Set to true to hide the history of the channel for added member. Default is false.
- **Response 200** (`AddChannelMemberResponseContent`)
  - `member` — ChannelMember **(required)**
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
- Errors: `400`, `403`, `404`, `409`, `429`

#### `PUT` `/v2/conversations/channels/{channelId}/members`

Adds members to an existing channel.
This operation is idempotent, meaning that if a member already exists in the channel, the operation will still return a successful response.
If some members cannot be added because their accounts are deactivated in GetStream, the operation still succeeds for the rest and returns skipped members in the response.


**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `AddChannelMembers`
- **Scopes**: `messaging:AddChannelMembers`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which members are to be added. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `AddChannelMembersRequestContent`)
  - `silent` — boolean — Set to true to suppress system messages that members were added to the conversation. Default is false.
  - `members` — array — A list of user IDs to be added as members of the channel.
    - _array of_ `string`
  - `membersToInvite` — array — A list of users to invite to the channel, identified by their email addresses or phone numbers.
    - _array of_ `UserToInvite`
      - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
      - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
      - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
  - `hideHistory` — boolean — Set to true to hide the history of the channel for added member. Default is false.
  - `unreadMessageId` — string — The unique identifier of the message that should be marked as unread for the added member. _(minLen=32; maxLen=32)_
- **Response 200** (`AddChannelMembersResponseContent`)
  - `members` — array **(required)** — The list of members added to the channel.
    - _array of_ `ChannelMember`
      - `id` — string **(required)**
      - `createdAt` — string **(required)**
      - `role` — string **(required)** _(enum: `member`, `supervisor`)_
  - `users` — array **(required)** — The list of users added to the channel.
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
  - `skippedMembers` — array **(required)** — The list of users skipped during the operation, for example because they are deactivated in GetStream.
    - _array of_ `SkippedMember`
      - `id` — string — The unique identifier of the skipped user if it is known. _(minLen=12; maxLen=12)_
      - `email` — string — The email address of the skipped user if it is known. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
      - `phone` — string — The phone number of the skipped user if it is known. _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/channels/{channelId}/members/{memberId}`

Retrieves details of a specific member in a channel. This includes the member's role and user information.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 100 |
| XBS | 3600 | 600 |
| PBX | 60 | 300 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 300 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetChannelMember`
- **Scopes**: `messaging:GetChannelMember`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `memberId` (path) — string **(required)** — The unique identifier of the user. _(minLen=12; maxLen=12)_
- **Response 200** (`GetChannelMemberResponseContent`)
  - `member` — ChannelMember **(required)**
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

#### `DELETE` `/v2/conversations/channels/{channelId}/members/{memberId}`

Deletes a specific member from a channel. This operation is idempotent, meaning that if the member does not exist, the operation will still return a successful response.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `DeleteChannelMember`
- **Scopes**: `messaging:DeleteChannelMember`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel from which the member is to be deleted. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `memberId` (path) — string **(required)** — The unique identifier of the member to be deleted. _(minLen=12; maxLen=12)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
  - `silent` (query) — boolean — Set to true to suppress system messages that the member was removed from the conversation. Default is false.
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/channels/{channelId}/read`

Retrieves a list of members read status for a specific channel. Read status does not work for conversations with more than 100 members.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 100 |
| XBS | 3600 | 600 |
| PBX | 60 | 300 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 300 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ListChannelMembersReadStatus`
- **Scopes**: `messaging:ListChannelMembersReadStatus`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel whose members are to be listed. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- **Response 200** (`ListChannelMembersReadStatusResponseContent`)
  - `members` — array **(required)** — Read status of members.
    - _array of_ `ChannelMemberReadStatus`
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
      - `lastRead` — string
      - `lastReadMessageId` — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/invite`

> ⚠️ Route marquée `deprecated` dans la spécification publiée.

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
- **Scopes**: `messaging:Invite`
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

### Messages

#### `GET` `/v2/conversations/channels/{channelId}/messages`

Retrieves a list of messages from a specified channel. Supports pagination through limit and offset parameters.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ListMessages`
- **Scopes**: `messaging:ListMessages`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel from which to list messages. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `limit` (query) — number — The maximum number of messages to return. The value must be between 1 and 100. _(min=1; max=100)_
  - `offset` (query) — number — The offset from which to start listing messages. The value must be between 0 and 1000. _(min=0; max=1000)_
- **Response 200** (`ListMessagesResponseContent`)
  - `messages` — array **(required)** — A list of messages from the specified channel.
    - _array of_ `Message`
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
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `quote` — MessageQuote
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `text` — string _(minLen=1; maxLen=5000)_
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `mentions` — array
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
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `createdAt` — string **(required)**
        - `updatedAt` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `edit` — boolean
      - `mentions` — array
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
      - `latestReactions` — array
        - _array of_ `Reaction`
          - `type` — string
          - `userId` — string _(minLen=12; maxLen=12)_
          - `messageId` — string
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
      - `reactionCounts` — ReactionCounts
        - _map of_ `number`
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/messages`

Sends a message to a specified channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 10 | 10 |
| XBS | 3600 | 600 |
| PBX | 10 | 30 |
| PBX | 3600 | 1800 |
| XBS_BOT | 10 | 30 |
| XBS_BOT | 3600 | 1800 |

- operationId: `SendMessage`
- **Scopes**: `messaging:SendMessage`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which the message is sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `SendMessageRequestContent`)
  - `text` — string _(minLen=1; maxLen=5000)_
  - `elements` — array
    - _array of_ `Element`
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
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
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `messageId` — string — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
  - `mentions` — array — A list of user IDs mentioned in the message.
    - _array of_ `string`
- **Response 200** (`SendMessageResponseContent`)
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
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
    - `latestReactions` — array
      - _array of_ `Reaction`
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/channels/{channelId}/messages/{messageId}`

Retrieves a specific message from a specified channel.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `GetMessage`
- **Scopes**: `messaging:GetMessage`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message to retrieve. _(minLen=32; maxLen=32)_
- **Response 200** (`GetMessageResponseContent`)
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
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
    - `latestReactions` — array
      - _array of_ `Reaction`
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/conversations/channels/{channelId}/messages/{messageId}`

Updates an existing message in a specified channel. This operation is idempotent and requires the channel and message to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `UpdateMessage`
- **Scopes**: `messaging:UpdateMessage`
- **Parameters**
  - `messageId` (path) — string **(required)** — The unique identifier of the message to update. _(minLen=32; maxLen=32)_
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UpdateMessageRequestContent`)
  - `text` — string _(minLen=1; maxLen=5000)_
  - `elements` — array
    - _array of_ `Element`
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
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
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `mentions` — array — A list of user IDs mentioned in the message.
    - _array of_ `string`
  - `silent` — boolean — Set to true to suppress the updated indicator. Defaults to false.
- **Response 200** (`UpdateMessageResponseContent`)
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
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
    - `latestReactions` — array
      - _array of_ `Reaction`
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `PATCH` `/v2/conversations/channels/{channelId}/messages/{messageId}`

Partially updates an existing message in a specified channel. This operation requires the channel and message to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `PartialUpdateMessage`
- **Scopes**: `messaging:PartialUpdateMessage`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message to update. _(minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `PartialUpdateMessageRequestContent`)
  - `set` — PartialUpdateMessageSetInput
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `mentions` — array — A list of user IDs mentioned in the message.
      - _array of_ `string`
  - `unset` — array — Fields to unset during the partial update.
    - _array of_ `MessageUnsetFields`
  - `silent` — boolean — Set to true to suppress the updated indicator. Defaults to false.
- **Response 200** (`PartialUpdateMessageResponseContent`)
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
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
    - `latestReactions` — array
      - _array of_ `Reaction`
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/conversations/channels/{channelId}/messages/{messageId}`

Deletes an existing message in a specified channel. This operation is idempotent and requires the channel and message to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `DeleteMessage`
- **Scopes**: `messaging:DeleteMessage`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message to delete. _(minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/conversations/channels/{channelId}/messages/{messageId}/pin`

Pins specified message in the message. This operation is idempotent, meaning that if the message is already pinned, no error will be thrown.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 10 | 10 |
| XBS | 3600 | 600 |
| PBX | 10 | 30 |
| PBX | 3600 | 1800 |
| XBS_BOT | 10 | 30 |
| XBS_BOT | 3600 | 1800 |

- operationId: `PinMessage`
- **Scopes**: `messaging:PinMessage`
- **Parameters**
  - `channelId` (path) — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message which should be pinned. _(minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `PinMessageRequestContent`)
  - `expiresAfter` — number — The duration in seconds after which the pinned message will be automatically unpinned. If neither `expiresAfter` nor `expiresAt` is provided, the message will remain pinned indefinitely. Providing both `expiresAfter` and `expiresAt` will result in a validation error.
  - `expiresAt` — string — The specific date and time (in ISO 8601 format) when the pinned message will be automatically unpinned. If neither `expiresAfter` nor `expiresAt` is provided, the message will remain pinned indefinitely. Providing both `expiresAfter` and `expiresAt` will result in a validation error.
  - `silent` — boolean — Set to true to suppress system messages generated by this operation. Defaults to false.
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/conversations/channels/{channelId}/messages/{messageId}/pin`

Unpins the message that was previously pinned. This operation is idempotent, meaning that if the message is not pinned, no error will be thrown.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 10 | 10 |
| XBS | 3600 | 600 |
| PBX | 10 | 30 |
| PBX | 3600 | 1800 |
| XBS_BOT | 10 | 30 |
| XBS_BOT | 3600 | 1800 |

- operationId: `UnpinMessage`
- **Scopes**: `messaging:UnpinMessage`
- **Parameters**
  - `channelId` (path) — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message which should be unpinned. _(minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
  - `silent` (query) — boolean — Set to true to suppress system messages generated by this operation. Defaults to false.
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/channels/{channelId}/messages/{messageId}/reactions`

Retrieves a list of reactions for a specific message in a specified channel. Supports pagination through limit and offset parameters.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ListMessageReactions`
- **Scopes**: `messaging:ListMessageReactions`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message whose reactions are to be listed. _(minLen=32; maxLen=32)_
  - `limit` (query) — number — The maximum number of reactions to return. The value must be between 1 and 300. _(min=1; max=300)_
  - `offset` (query) — number — The offset from which to start listing reactions. The value must be between 0 and 1000. _(min=0; max=1000)_
- **Response 200** (`ListMessageReactionsResponseContent`)
  - `reactions` — array **(required)** — A list of reactions to the specified message.
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
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
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/messages/{messageId}/reactions`

Sends a reaction to a specific message in a specified channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `SendMessageReaction`
- **Scopes**: `messaging:SendMessageReaction`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message to which the reaction is sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `SendMessageReactionRequestContent`) **(required)**
  - `reactionType` — string **(required)** _(enum: `thumbsup`, `clap`, `slightly_smiling_face`, `smiley`, `heart`, `eyes`, `white_check_mark`, `confused`, `thumbsdown`)_
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/conversations/channels/{channelId}/messages/{messageId}/reactions/{reactionType}`

Deletes a reaction from a specific message in a specified channel. This operation is idempotent and requires the channel and message to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `DeleteMessageReaction`
- **Scopes**: `messaging:DeleteMessageReaction`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message to delete the reaction from. _(minLen=32; maxLen=32)_
  - `reactionType` (path) — string **(required)** — The type of the reaction to delete. _(enum: `thumbsup`, `clap`, `slightly_smiling_face`, `smiley`, `heart`, `eyes`, `white_check_mark`, `confused`, `thumbsdown`)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/channels/{channelId}/pinned_messages`

Retrieves a list of pinned messages from a specified channel. Supports pagination through limit and offset parameters.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ListPinnedMessages`
- **Scopes**: `messaging:ListPinnedMessages`, `messaging:read`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel from which to list messages. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `limit` (query) — number — The maximum number of pinned messages to return. The value must be between 1 and 100. _(min=1; max=100)_
  - `offset` (query) — number — The offset from which to start listing pinned messages. The value must be between 0 and 1000. _(min=0; max=1000)_
- **Response 200** (`ListPinnedMessagesResponseContent`)
  - `messages` — array **(required)** — A list of pinned messages in the channel.
    - _array of_ `Message`
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
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `quote` — MessageQuote
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `text` — string _(minLen=1; maxLen=5000)_
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `mentions` — array
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
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `createdAt` — string **(required)**
        - `updatedAt` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `edit` — boolean
      - `mentions` — array
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
      - `latestReactions` — array
        - _array of_ `Reaction`
          - `type` — string
          - `userId` — string _(minLen=12; maxLen=12)_
          - `messageId` — string
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
      - `reactionCounts` — ReactionCounts
        - _map of_ `number`
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/send_giphy`

Sends a Giphy message to a specified channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `SendGiphy`
- **Scopes**: `messaging:SendGiphy`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which the Giphy message is sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `SendGiphyRequestContent`) **(required)**
  - `messageId` — string — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
  - `giphy` — MessageGiphy **(required)**
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
- **Response 200** (`SendGiphyResponseContent`)
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
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
    - `latestReactions` — array
      - _array of_ `Reaction`
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/send_typing_start`

Sends a typing start event to a specified channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `SendTypingStart`
- **Scopes**: `messaging:SendTypingStart`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which the typing start event is sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/send_typing_stop`

Sends a typing stop event to a specified channel. This operation requires the channel to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 50 |
| XBS | 3600 | 600 |
| PBX | 60 | 150 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 150 |
| XBS_BOT | 3600 | 1800 |

- operationId: `SendTypingStop`
- **Scopes**: `messaging:SendTypingStop`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which the typing stop event is sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/channels/{channelId}/system-messages`

Sends a system message to a specified channel. This operation available with S2S authorization only.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| S2S | 10 | 30 |
| S2S | 3600 | 1800 |

- operationId: `SendSystemMessage`
- **Scopes**: `messaging:SendSystemMessage`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which the message is sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- **Request body** (`application/json` — `SendSystemMessageRequestContent`) **(required)**
  - `userId` — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
  - `message` — union **(required)**
    - _oneOf_ — exactly one of:
      - **`whatsAppClosed`**
        - `whatsAppClosed` — WhatsAppClosedSystemMessage **(required)**
      - **`multipleMembersJoined`**
        - `multipleMembersJoined` — MultipleMembersJoinedSystemMessage **(required)**
          - `addedMembers` — array **(required)**
            - _array of_ `string`
- **Response 200** (`SendSystemMessageResponseContent`)
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _oneOf_ — exactly one of:
          - **`template`**
            - `template` — MessageTemplateConfig **(required)**
              - `whatsapp` — TemplateWithParameters
                - _(nesting depth limit — see `TemplateWithParameters` in the Schemas appendix)_
          - **`actions`**
            - `actions` — array **(required)**
              - _array of_ `ActionElement`
                - _(nesting depth limit — see `ActionElement` in the Schemas appendix)_
          - **`wilma`**
            - `wilma` — WilmaChatElement **(required)** — On every agent reply of a Wilma chat on the stream transport: the session and turn that produced it, how the turn went and what it shared. `verbosity` is the agent's setting when the session started; clients decide from it what to show. The turn's events are `startIndex`..`endIndex` of the session log: read them with GetSessionEvents(sessionId, startIndex).
              - `sessionId` — string **(required)** _(minLen=1; maxLen=64)_
              - `verbosity` — string **(required)** — How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text. _(enum: `none`, `simple`, `full`)_
              - `turn` — number **(required)** — The turn of the session that produced this message. A steer that joins a running turn shares it. _(min=1)_
              - `startIndex` — number **(required)** — Index of the turn's first event (`turnStarted`) in the session log. _(min=0)_
              - `endIndex` — number — Index of the turn's last event (completed, failed or stopped). Absent when the message was written before the turn ended. _(min=0)_
              - `summary` — WilmaChatTurnSummary **(required)** — How the turn went. The calls themselves (input, output) are not stored here: they are the turn's events in the session log.
                - _(nesting depth limit — see `WilmaChatTurnSummary` in the Schemas appendix)_
              - `artifacts` — array
                - _(nesting depth limit — see `WilmaChatArtifact` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - `id` — string **(required)**
        - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
        - `mime` — string
        - `name` — string **(required)**
        - `size` — number **(required)**
        - `width` — number
        - `height` — number
        - `thumbnail` — string
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _array of_ `MessageAttachment`
          - `id` — string **(required)**
          - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
          - `mime` — string
          - `name` — string **(required)**
          - `size` — number **(required)**
          - `width` — number
          - `height` — number
          - `thumbnail` — string
      - `forward` — MessageForward
        - `forwardCompany` — string
        - `forwardDate` — string **(required)**
        - `forwardEmail` — string
        - `forwardName` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `mentions` — array
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
      - `giphy` — MessageGiphy
        - `id` — string **(required)** _(minLen=1)_
        - `size` — string **(required)** _(pattern=^\d+$)_
        - `url` — string **(required)** _(minLen=1)_
        - `height` — string **(required)** _(pattern=^\d+$)_
        - `width` — string **(required)** _(pattern=^\d+$)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
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
    - `latestReactions` — array
      - _array of_ `Reaction`
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
- Errors: `400`, `403`, `404`, `429`

#### `PUT` `/v2/conversations/inbox/tags/{tagId}`

Updates an existing tag. This operation is idempotent.

- operationId: `UpdateInboxTag`
- **Scopes**: `messaging:UpdateInboxTag`
- **Parameters**
  - `tagId` (path) — string **(required)** — The unique identifier of the channel containing the message. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `UpdateInboxTagRequestContent`) **(required)**
  - `name` — string **(required)** — The name of the tag. _(minLen=1; maxLen=80)_
- **Response 200** (`UpdateInboxTagResponseContent`)
  - `tag` — InboxTag **(required)**
    - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
    - `name` — string **(required)** _(minLen=1; maxLen=80)_
- Errors: `400`, `403`, `404`, `429`

#### `DELETE` `/v2/conversations/inbox/tags/{tagId}`

Deletes an existing tag. This operation is idempotent.

- operationId: `DeleteInboxTag`
- **Scopes**: `messaging:DeleteInboxTag`
- **Parameters**
  - `tagId` (path) — string **(required)** — The unique identifier of the tag. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `429`

### Actions

#### `POST` `/v2/conversations/channels/{channelId}/messages/{messageId}/actions/{actionId}/trigger`

Sends a trigger for specific action for specified message. This operation requires the message to be accessible to the user.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 10 | 10 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 10 | 10 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 10 | 30 |
| PBX | 3600 | 1800 |

- operationId: `TriggerMessageAction`
- **Scopes**: `messaging:TriggerMessageAction`
- **Parameters**
  - `channelId` (path) — string **(required)** — The unique identifier of the channel to which the message is sent. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `messageId` (path) — string **(required)** — The unique identifier of the message which hold an action. _(minLen=32; maxLen=32)_
  - `actionId` (path) — string **(required)** — The unique identifier of the action inside the message. _(minLen=1; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`TriggerMessageActionResponseContent`)
  - `triggerId` — string **(required)** _(minLen=32; maxLen=32)_
- Errors: `400`, `403`, `404`, `429`

#### `GET` `/v2/conversations/triggers/{triggerId}/result`

Get result of the triggered action.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 10 | 10 |
| XBS | 3600 | 600 |
| XBS_ANONYMOUS | 10 | 10 |
| XBS_ANONYMOUS | 3600 | 600 |
| PBX | 10 | 30 |
| PBX | 3600 | 1800 |

- operationId: `GetActionTriggerResult`
- **Scopes**: `messaging:GetActionTriggerResult`
- **Parameters**
  - `triggerId` (path) — string **(required)** — The unique identifier of the action trigger inside the message. _(minLen=32; maxLen=32)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`GetActionTriggerResultResponseContent`)
  - `status` — string **(required)** _(enum: `completed`, `pending`)_
  - `result` — ActionTriggerResult
    - `url` — string _(minLen=3; maxLen=2048)_
- Errors: `400`, `403`, `404`, `429`

#### `POST` `/v2/conversations/triggers/{triggerId}/result`

Send result of the triggered action.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| PBX | 10 | 30 |
| PBX | 3600 | 1800 |
| XBS_BOT | 10 | 30 |
| XBS_BOT | 3600 | 1800 |

- operationId: `SendActionTriggerResult`
- **Scopes**: `messaging:SendActionTriggerResult`
- **Parameters**
  - `triggerId` (path) — string **(required)** — The unique identifier of the action trigger inside the message. _(minLen=32; maxLen=32)_
- **Request body** (`application/json` — `SendActionTriggerResultRequestContent`) **(required)**
  - `status` — string **(required)** _(enum: `completed`, `pending`)_
  - `result` — ActionTriggerResult **(required)**
    - `url` — string _(minLen=3; maxLen=2048)_
- Errors: `400`, `403`, `404`, `429`

### Other

#### `POST` `/v2/conversations/describe`

- operationId: `DescribeEvent`
- **Scopes**: `messaging:DescribeEvent`
- **Response 200** (`DescribeEventResponseContent`)
  - `WebhookChatChannelCreatedEvent` — WebhookChatChannelCreatedEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatChannelCreatedOrUpdatedEventData **(required)**
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
      - `members` — array **(required)**
        - _array of_ `ChannelMember`
          - `id` — string **(required)**
          - `createdAt` — string **(required)**
          - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
  - `WebhookChatChannelUpdatedEvent` — WebhookChatChannelUpdatedEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatChannelCreatedOrUpdatedEventData **(required)**
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
      - `members` — array **(required)**
        - _array of_ `ChannelMember`
          - `id` — string **(required)**
          - `createdAt` — string **(required)**
          - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
  - `WebhookChatMemberAddedEvent` — WebhookChatMemberAddedEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatMemberAddedOrRemovedEventData **(required)**
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
      - `member` — ChannelMember **(required)**
        - `id` — string **(required)**
        - `createdAt` — string **(required)**
        - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
  - `WebhookChatMemberRemovedEvent` — WebhookChatMemberRemovedEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatMemberAddedOrRemovedEventData **(required)**
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
      - `member` — ChannelMember **(required)**
        - `id` — string **(required)**
        - `createdAt` — string **(required)**
        - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
  - `WebhookChatMessageNewEvent` — WebhookChatMessageNewEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatMessageNewEventData **(required)**
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
      - `members` — array **(required)**
        - _array of_ `ChannelMember`
          - `id` — string **(required)**
          - `createdAt` — string **(required)**
          - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
      - `message` — Message **(required)**
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
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `quote` — MessageQuote
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
          - `text` — string _(minLen=1; maxLen=5000)_
          - `attachments` — array
            - _array of_ `MessageAttachment`
              - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
          - `forward` — MessageForward
            - `forwardCompany` — string
            - `forwardDate` — string **(required)**
            - `forwardEmail` — string
            - `forwardName` — string
            - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
            - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `mentions` — array
            - _array of_ `User`
              - _(nesting depth limit — see `User` in the Schemas appendix)_
          - `giphy` — MessageGiphy
            - `id` — string **(required)** _(minLen=1)_
            - `size` — string **(required)** _(pattern=^\d+$)_
            - `url` — string **(required)** _(minLen=1)_
            - `height` — string **(required)** _(pattern=^\d+$)_
            - `width` — string **(required)** _(pattern=^\d+$)_
          - `createdAt` — string **(required)**
          - `updatedAt` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `whatsapp` — boolean
        - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
        - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
        - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
        - `sms` — boolean
        - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
        - `markdown` — boolean
        - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `silent` — boolean
        - `event` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `edit` — boolean
        - `mentions` — array
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
        - `latestReactions` — array
          - _array of_ `Reaction`
            - `type` — string
            - `userId` — string _(minLen=12; maxLen=12)_
            - `messageId` — string
            - `user` — User
              - _(nesting depth limit — see `User` in the Schemas appendix)_
        - `reactionCounts` — ReactionCounts
          - _map of_ `number`
        - `createdAt` — string **(required)**
        - `updatedAt` — string
  - `WebhookChatMessageUpdatedEvent` — WebhookChatMessageUpdatedEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatMessageUpdatedOrDeletedEventData **(required)**
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
      - `message` — Message **(required)**
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
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `quote` — MessageQuote
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
          - `text` — string _(minLen=1; maxLen=5000)_
          - `attachments` — array
            - _array of_ `MessageAttachment`
              - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
          - `forward` — MessageForward
            - `forwardCompany` — string
            - `forwardDate` — string **(required)**
            - `forwardEmail` — string
            - `forwardName` — string
            - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
            - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `mentions` — array
            - _array of_ `User`
              - _(nesting depth limit — see `User` in the Schemas appendix)_
          - `giphy` — MessageGiphy
            - `id` — string **(required)** _(minLen=1)_
            - `size` — string **(required)** _(pattern=^\d+$)_
            - `url` — string **(required)** _(minLen=1)_
            - `height` — string **(required)** _(pattern=^\d+$)_
            - `width` — string **(required)** _(pattern=^\d+$)_
          - `createdAt` — string **(required)**
          - `updatedAt` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `whatsapp` — boolean
        - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
        - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
        - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
        - `sms` — boolean
        - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
        - `markdown` — boolean
        - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `silent` — boolean
        - `event` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `edit` — boolean
        - `mentions` — array
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
        - `latestReactions` — array
          - _array of_ `Reaction`
            - `type` — string
            - `userId` — string _(minLen=12; maxLen=12)_
            - `messageId` — string
            - `user` — User
              - _(nesting depth limit — see `User` in the Schemas appendix)_
        - `reactionCounts` — ReactionCounts
          - _map of_ `number`
        - `createdAt` — string **(required)**
        - `updatedAt` — string
  - `WebhookChatMessageDeletedEvent` — WebhookChatMessageDeletedEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatMessageUpdatedOrDeletedEventData **(required)**
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
      - `message` — Message **(required)**
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
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `quote` — MessageQuote
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
          - `text` — string _(minLen=1; maxLen=5000)_
          - `attachments` — array
            - _array of_ `MessageAttachment`
              - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
          - `forward` — MessageForward
            - `forwardCompany` — string
            - `forwardDate` — string **(required)**
            - `forwardEmail` — string
            - `forwardName` — string
            - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
            - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `mentions` — array
            - _array of_ `User`
              - _(nesting depth limit — see `User` in the Schemas appendix)_
          - `giphy` — MessageGiphy
            - `id` — string **(required)** _(minLen=1)_
            - `size` — string **(required)** _(pattern=^\d+$)_
            - `url` — string **(required)** _(minLen=1)_
            - `height` — string **(required)** _(pattern=^\d+$)_
            - `width` — string **(required)** _(pattern=^\d+$)_
          - `createdAt` — string **(required)**
          - `updatedAt` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `whatsapp` — boolean
        - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
        - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
        - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
        - `sms` — boolean
        - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
        - `markdown` — boolean
        - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `silent` — boolean
        - `event` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `edit` — boolean
        - `mentions` — array
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
        - `latestReactions` — array
          - _array of_ `Reaction`
            - `type` — string
            - `userId` — string _(minLen=12; maxLen=12)_
            - `messageId` — string
            - `user` — User
              - _(nesting depth limit — see `User` in the Schemas appendix)_
        - `reactionCounts` — ReactionCounts
          - _map of_ `number`
        - `createdAt` — string **(required)**
        - `updatedAt` — string
  - `WebhookChatReactionNewEvent` — WebhookChatReactionNewEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatReactionNewOrDeletedEventData **(required)**
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
      - `message` — Message **(required)**
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
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `quote` — MessageQuote
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
          - `text` — string _(minLen=1; maxLen=5000)_
          - `attachments` — array
            - _array of_ `MessageAttachment`
              - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
          - `forward` — MessageForward
            - `forwardCompany` — string
            - `forwardDate` — string **(required)**
            - `forwardEmail` — string
            - `forwardName` — string
            - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
            - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `mentions` — array
            - _array of_ `User`
              - _(nesting depth limit — see `User` in the Schemas appendix)_
          - `giphy` — MessageGiphy
            - `id` — string **(required)** _(minLen=1)_
            - `size` — string **(required)** _(pattern=^\d+$)_
            - `url` — string **(required)** _(minLen=1)_
            - `height` — string **(required)** _(pattern=^\d+$)_
            - `width` — string **(required)** _(pattern=^\d+$)_
          - `createdAt` — string **(required)**
          - `updatedAt` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `whatsapp` — boolean
        - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
        - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
        - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
        - `sms` — boolean
        - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
        - `markdown` — boolean
        - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `silent` — boolean
        - `event` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `edit` — boolean
        - `mentions` — array
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
        - `latestReactions` — array
          - _array of_ `Reaction`
            - `type` — string
            - `userId` — string _(minLen=12; maxLen=12)_
            - `messageId` — string
            - `user` — User
              - _(nesting depth limit — see `User` in the Schemas appendix)_
        - `reactionCounts` — ReactionCounts
          - _map of_ `number`
        - `createdAt` — string **(required)**
        - `updatedAt` — string
      - `reaction` — Reaction **(required)**
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
  - `WebhookChatReactionDeletedEvent` — WebhookChatReactionDeletedEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatReactionNewOrDeletedEventData **(required)**
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
      - `message` — Message **(required)**
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
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `quote` — MessageQuote
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
          - `text` — string _(minLen=1; maxLen=5000)_
          - `attachments` — array
            - _array of_ `MessageAttachment`
              - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
          - `forward` — MessageForward
            - `forwardCompany` — string
            - `forwardDate` — string **(required)**
            - `forwardEmail` — string
            - `forwardName` — string
            - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
            - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `mentions` — array
            - _array of_ `User`
              - _(nesting depth limit — see `User` in the Schemas appendix)_
          - `giphy` — MessageGiphy
            - `id` — string **(required)** _(minLen=1)_
            - `size` — string **(required)** _(pattern=^\d+$)_
            - `url` — string **(required)** _(minLen=1)_
            - `height` — string **(required)** _(pattern=^\d+$)_
            - `width` — string **(required)** _(pattern=^\d+$)_
          - `createdAt` — string **(required)**
          - `updatedAt` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `whatsapp` — boolean
        - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
        - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
        - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
        - `sms` — boolean
        - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
        - `markdown` — boolean
        - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `silent` — boolean
        - `event` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `edit` — boolean
        - `mentions` — array
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
        - `latestReactions` — array
          - _array of_ `Reaction`
            - `type` — string
            - `userId` — string _(minLen=12; maxLen=12)_
            - `messageId` — string
            - `user` — User
              - _(nesting depth limit — see `User` in the Schemas appendix)_
        - `reactionCounts` — ReactionCounts
          - _map of_ `number`
        - `createdAt` — string **(required)**
        - `updatedAt` — string
      - `reaction` — Reaction **(required)**
        - `type` — string
        - `userId` — string _(minLen=12; maxLen=12)_
        - `messageId` — string
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
  - `WebhookChatActionTriggeredEvent` — WebhookChatActionTriggeredEvent
    - `id` — string **(required)**
    - `company` — string **(required)**
    - `type` — object **(required)**
    - `time` — number **(required)**
    - `integrationId` — string
    - `botId` — string
    - `data` — WebhookChatActionTriggeredEventData **(required)**
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
      - `message` — Message **(required)**
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
        - `attachments` — array
          - _array of_ `MessageAttachment`
            - `id` — string **(required)**
            - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
            - `mime` — string
            - `name` — string **(required)**
            - `size` — number **(required)**
            - `width` — number
            - `height` — number
            - `thumbnail` — string
        - `quote` — MessageQuote
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
          - `text` — string _(minLen=1; maxLen=5000)_
          - `attachments` — array
            - _array of_ `MessageAttachment`
              - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
          - `forward` — MessageForward
            - `forwardCompany` — string
            - `forwardDate` — string **(required)**
            - `forwardEmail` — string
            - `forwardName` — string
            - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
            - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
          - `mentions` — array
            - _array of_ `User`
              - _(nesting depth limit — see `User` in the Schemas appendix)_
          - `giphy` — MessageGiphy
            - `id` — string **(required)** _(minLen=1)_
            - `size` — string **(required)** _(pattern=^\d+$)_
            - `url` — string **(required)** _(minLen=1)_
            - `height` — string **(required)** _(pattern=^\d+$)_
            - `width` — string **(required)** _(pattern=^\d+$)_
          - `createdAt` — string **(required)**
          - `updatedAt` — string
        - `forward` — MessageForward
          - `forwardCompany` — string
          - `forwardDate` — string **(required)**
          - `forwardEmail` — string
          - `forwardName` — string
          - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
          - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `whatsapp` — boolean
        - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
        - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
        - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
        - `sms` — boolean
        - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
        - `markdown` — boolean
        - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
        - `giphy` — MessageGiphy
          - `id` — string **(required)** _(minLen=1)_
          - `size` — string **(required)** _(pattern=^\d+$)_
          - `url` — string **(required)** _(minLen=1)_
          - `height` — string **(required)** _(pattern=^\d+$)_
          - `width` — string **(required)** _(pattern=^\d+$)_
        - `silent` — boolean
        - `event` — string
        - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
        - `edit` — boolean
        - `mentions` — array
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
        - `latestReactions` — array
          - _array of_ `Reaction`
            - `type` — string
            - `userId` — string _(minLen=12; maxLen=12)_
            - `messageId` — string
            - `user` — User
              - _(nesting depth limit — see `User` in the Schemas appendix)_
        - `reactionCounts` — ReactionCounts
          - _map of_ `number`
        - `createdAt` — string **(required)**
        - `updatedAt` — string
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
      - `actionId` — string **(required)**
      - `triggerId` — string **(required)**
- Errors: `400`, `403`, `429`

### Inbox

#### `GET` `/v2/conversations/inbox/state`

Retrieves the user's inbox state to track pinned, tagged, and unread markers.

- operationId: `GetInboxState`
- **Scopes**: `messaging:GetInboxState`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`GetInboxStateResponseContent`)
  - `channels` — InboxChannelsState **(required)**
    - `unread` — array **(required)**
      - _array of_ `InboxUnreadChannel`
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `unreadAt` — string **(required)** — A date when unread indicator was set by the user.
        - `messageId` — string _(minLen=32; maxLen=32)_
    - `pinned` — array **(required)**
      - _array of_ `InboxPinnedChannel`
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `pinnedAt` — string **(required)**
    - `tagged` — array **(required)**
      - _array of_ `InboxTaggedChannel`
        - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
        - `tagId` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `tags` — array **(required)**
    - _array of_ `InboxTag`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
      - `name` — string **(required)** _(minLen=1; maxLen=80)_
- Errors: `400`, `403`, `429`

#### `GET` `/v2/conversations/inbox/tags`

Returns a list of tags associated with the user.

- operationId: `ListInboxTags`
- **Scopes**: `messaging:ListInboxTags`, `messaging:read`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`ListInboxTagsResponseContent`)
  - `tags` — array **(required)**
    - _array of_ `InboxTag`
      - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
      - `name` — string **(required)** _(minLen=1; maxLen=80)_
- Errors: `400`, `403`, `429`

#### `POST` `/v2/conversations/inbox/tags`

Creates a new tag that can be used to group channels. Each user can have up to 15 tags. If the limit is reached, a TagsLimitReachedException will be thrown.

- operationId: `CreateInboxTag`
- **Scopes**: `messaging:CreateInboxTag`
- **Parameters**
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Request body** (`application/json` — `CreateInboxTagRequestContent`) **(required)**
  - `tagId` — string — The unique identifier for the new group channel. If not provided, the system will generate one. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `name` — string **(required)** — The name of the tag. _(minLen=1; maxLen=80)_
- **Response 200** (`CreateInboxTagResponseContent`)
  - `tag` — InboxTag **(required)**
    - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
    - `name` — string **(required)** _(minLen=1; maxLen=80)_
- Errors: `400`, `403`, `429`

#### `GET` `/v2/conversations/inbox/tags/{tagId}`

Returns a list of channels associated with the specified tag.

- operationId: `ListInboxTaggedChannels`
- **Scopes**: `messaging:ListInboxTaggedChannels`, `messaging:read`
- **Parameters**
  - `tagId` (path) — string **(required)** — The unique identifier of the channel whose members are to be listed. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `user` (query) — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- **Response 200** (`ListInboxTaggedChannelsResponseContent`)
  - `channels` — array **(required)**
    - _array of_ `InboxTaggedChannel`
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `tagId` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
- Errors: `400`, `403`, `404`, `429`

### Jobs

#### `POST` `/v2/conversations/schedule_external_flag_adjustment_job`

Schedules a job to fix the "external" flag for channels in which the user participates.

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 20 |
| XBS | 3600 | 600 |
| PBX | 60 | 60 |
| PBX | 3600 | 1800 |
| XBS_BOT | 60 | 60 |
| XBS_BOT | 3600 | 1800 |

- operationId: `ScheduleExternalFlagAdjustmentJob`
- **Scopes**: `messaging:ScheduleExternalFlagAdjustmentJob`
- **Request body** (`application/json` — `ScheduleExternalFlagAdjustmentJobRequestContent`) **(required)**
  - `userId` — string **(required)** — The unique identifier of the user. _(minLen=12; maxLen=12)_
- Errors: `400`, `403`, `429`, `500`

### Auth

#### `GET` `/v2/conversations/token`

Retrieve an authorization token for chat.wildix-chat.com

**Rate Limits**
| Authorization Type | Period (seconds) | Requests by period |
| --- | :---: | :---: |
| XBS | 60 | 10 |
| XBS | 3600 | 60 |
| XBS_ANONYMOUS | 60 | 10 |
| XBS_ANONYMOUS | 3600 | 60 |

- operationId: `GetToken`
- **Scopes**: `messaging:GetToken`, `messaging:read`
- **Parameters**
  - `clientId` (query) — string — Client ID for GetStream, based on which the correct token will be issued and signed
- **Response 200** (`GetTokenResponseContent`)
  - `token` — string **(required)** — An authorization token.
  - `expires` — number **(required)** — A token's expiration time.
- Errors: `400`, `403`, `429`

### Schemas appendix — Conversations API

<details><summary>188 component schemas</summary>

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

**`ActionTriggerResult`**

- `url` — string _(minLen=3; maxLen=2048)_

**`ActionTriggerStatus`**

- string _(enum: `completed`, `pending`)_

**`AddChannelMemberRequestContent`**

- `silent` — boolean — True to not send a system message that members added from the conversartion. Default - false.
- `memberId` — string — A User ID of the member to be added to the channel. _(minLen=12; maxLen=12)_
- `memberToInvite` — UserToInvite
  - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
  - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
- `hideHistory` — boolean — Set to true to hide the history of the channel for added member. Default is false.

**`AddChannelMemberResponseContent`**

- `member` — ChannelMember **(required)**
  - `id` — string **(required)**
  - `createdAt` — string **(required)**
  - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`AddChannelMembersRequestContent`**

- `silent` — boolean — Set to true to suppress system messages that members were added to the conversation. Default is false.
- `members` — array — A list of user IDs to be added as members of the channel.
  - _array of_ `string`
- `membersToInvite` — array — A list of users to invite to the channel, identified by their email addresses or phone numbers.
  - _array of_ `UserToInvite`
    - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
    - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
- `hideHistory` — boolean — Set to true to hide the history of the channel for added member. Default is false.
- `unreadMessageId` — string — The unique identifier of the message that should be marked as unread for the added member. _(minLen=32; maxLen=32)_

**`AddChannelMembersResponseContent`**

- `members` — array **(required)** — The list of members added to the channel.
  - _array of_ `ChannelMember`
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
- `users` — array **(required)** — The list of users added to the channel.
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
- `skippedMembers` — array **(required)** — The list of users skipped during the operation, for example because they are deactivated in GetStream.
  - _array of_ `SkippedMember`
    - `id` — string — The unique identifier of the skipped user if it is known. _(minLen=12; maxLen=12)_
    - `email` — string — The email address of the skipped user if it is known. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the skipped user if it is known. _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_

**`AssignChannelAssigneeRequest`**

- _oneOf_ — exactly one of:
  - **`id`**
    - `id` — string **(required)** — A User ID of the assignee.
  - **`email`**
    - `email` — string **(required)** — An email of the assignee.

**`AssignChannelRequestContent`**

- `silent` — boolean — True to not send a system message that channel was assigned to specific service or user. Default - false.
- `service` — union
  - _oneOf_ — exactly one of:
    - **`uri`**
      - `uri` — string **(required)** — A unique identifier of the service. URI structure - <serviceId>@<pbxDomain>:<pbxPort> (example 1@demo.wildix.com:433) _(pattern=^\d+@.+:\d+$)_
- `assignee` — union
  - _oneOf_ — exactly one of:
    - **`id`**
      - `id` — string **(required)** — A User ID of the assignee.
    - **`email`**
      - `email` — string **(required)** — An email of the assignee.
- `variant` — string _(enum: `ADAPTIVE`, `SELECTED`, `EVERYBODY`, `SKIP`)_

**`AssignChannelResponseContent`**

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

**`AssignChannelServiceRequest`**

- _oneOf_ — exactly one of:
  - **`uri`**
    - `uri` — string **(required)** — A unique identifier of the service. URI structure - <serviceId>@<pbxDomain>:<pbxPort> (example 1@demo.wildix.com:433) _(pattern=^\d+@.+:\d+$)_

**`AssignChannelVariant`**

- string _(enum: `ADAPTIVE`, `SELECTED`, `EVERYBODY`, `SKIP`)_

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

**`ButtonVariant`**

- string _(enum: `contained`, `outlined`)_

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

**`ChannelAlreadyExistExceptionResponseContent`**

- `message` — string **(required)**

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

**`ChannelMember`**

- `id` — string **(required)**
- `createdAt` — string **(required)**
- `role` — string **(required)** _(enum: `member`, `supervisor`)_

**`ChannelMemberReadStatus`**

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
- `lastRead` — string
- `lastReadMessageId` — string

**`ChannelMemberRole`**

- string _(enum: `member`, `supervisor`)_

**`ChannelMessagingStatus`**

_Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window._

- string _(enum: `window_closed`)_

**`ChannelNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`ChannelType`**

- string _(enum: `direct`, `group`)_

**`ChannelWhatsAppStatus`**

- string _(enum: `24h_channel_closed`)_

**`ChannelsQuery`**

- `ids` — array _(maxItems=30)_
  - _array of_ `string`

**`ChatVerbosity`**

_How much of a chat turn x-bees shows while the agent works. SMS and WhatsApp always send one final text._

- string _(enum: `none`, `simple`, `full`)_

**`ConversationFileCategory`**

- string _(enum: `channels`, `recordings`, `wizyconfRecordings`)_

**`ConversationsServiceExceptionResponseContent`**

- `message` — string **(required)**

**`CreateGroupChannelRequestContent`**

- `subject` — string — The subject of the channel. _(minLen=1; maxLen=80)_
- `description` — string — The description of the channel. _(maxLen=160)_
- `picture` — string — The URL of the channel's picture. _(pattern=^https://[^\s/$.?#].[^\s]*$)_
- `pictureColor` — string — The dominant color of the channel's picture, represented by a hex value. _(pattern=^#[0-9a-fA-F]{6}$)_
- `access` — string _(enum: `private`, `public`)_
- `broadcast` — boolean — Indicates if the channel is broadcast-only. Default is false.
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
- `whatsappStatus` — string _(enum: `24h_channel_closed`)_
- `sms` — boolean — Indicates if the channel supports SMS. Default is false.
- `mms` — boolean — Indicates if the channel supports MMS. Default is false.
- `whatsapp` — boolean — Indicates if the channel supports WhatsApp. Default is false.
- `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
- `messagingSenderId` — string — The business side of the conversation: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. A reply has to name the sender it is sent from. On Messenger and Instagram kite writes it from the inbound event, because the channel id hashes the sender's linked service and not the sender; on RCS the channel id includes the brand, and it is written when the channel is created.
- `messagingReplyUntil` — number — Epoch seconds until which a reply still reaches the person. On Messenger and Instagram this is Meta's 7 day HUMAN_AGENT deadline, restarted by each inbound message; classound applies the tag itself, so this is the one deadline a client has to show. 0 means the deadline is not known, which is what the inbound event carries when the session row was gone before it could be read back; it does not mean the window has closed, so a client reads the window as closed on `messagingReplyUntil > 0 && now > messagingReplyUntil` and shows nothing at 0. Absent on a channel with no reply window.
- `kiteAssign` — string — The unique identifier of the assignee.
- `serviceTitle` — string
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
- `autoRecord` — boolean
- `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
- `transcriptionLanguage` — string
- `wizyGuestViewOnly` — boolean
- `channelId` — string — The unique identifier for the new group channel. If not provided, the system will generate one. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `members` — array — A list of user IDs to be added as members of the group channel.
  - _array of_ `string`
- `membersToInvite` — array — A list of users to invite to the group channel, identified by their email addresses or phone numbers.
  - _array of_ `UserToInvite`
    - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
    - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
    - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
    - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.
- `creationEventType` — string — Defines which system event is emitted when a group channel is created. _(enum: `conversation_created`, `conversation_created_with_name`)_

**`CreateGroupChannelResponseContent`**

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

**`CreateInboxTagRequestContent`**

- `tagId` — string — The unique identifier for the new group channel. If not provided, the system will generate one. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
- `name` — string **(required)** — The name of the tag. _(minLen=1; maxLen=80)_

**`CreateInboxTagResponseContent`**

- `tag` — InboxTag **(required)**
  - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `name` — string **(required)** _(minLen=1; maxLen=80)_

**`CreateKiteChannelRequestContent`**

- `channelId` — string — The unique identifier for the new group channel. If not provided, the system will generate one. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `targetId` — string **(required)** — The unique identifier of the Kite widget or email of the agent (example: 36cv69ao or vadim.ruban@wildix.com).
- `targetRouteId` — string — The unique identifier of the route for time-based configuration.
- `welcomeMessages` — array — A list of welcome messages is created during channel creation to preserve the same state as the client has on the interface. If welcomeMessages or initialMessage are not specified, the system will generate a 'conversation was created' system message.
  - _array of_ `WelcomeMessage`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `messageId` — string **(required)** — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
    - `mentions` — array — A list of user IDs mentioned in the message.
      - _array of_ `string`
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
- `initialMessage` — InitialMessage
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `messageId` — string **(required)** — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
  - `mentions` — array — A list of user IDs mentioned in the message.
    - _array of_ `string`

**`CreateKiteChannelResponseContent`**

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

**`DescribeEventResponseContent`**

- `WebhookChatChannelCreatedEvent` — WebhookChatChannelCreatedEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatChannelCreatedOrUpdatedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `members` — array **(required)**
      - _array of_ `ChannelMember`
        - _(nesting depth limit — see `ChannelMember` in the Schemas appendix)_
    - `users` — array **(required)**
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
- `WebhookChatChannelUpdatedEvent` — WebhookChatChannelUpdatedEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatChannelCreatedOrUpdatedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `members` — array **(required)**
      - _array of_ `ChannelMember`
        - _(nesting depth limit — see `ChannelMember` in the Schemas appendix)_
    - `users` — array **(required)**
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
- `WebhookChatMemberAddedEvent` — WebhookChatMemberAddedEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatMemberAddedOrRemovedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `member` — ChannelMember **(required)**
      - `id` — string **(required)**
      - `createdAt` — string **(required)**
      - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
- `WebhookChatMemberRemovedEvent` — WebhookChatMemberRemovedEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatMemberAddedOrRemovedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `member` — ChannelMember **(required)**
      - `id` — string **(required)**
      - `createdAt` — string **(required)**
      - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
- `WebhookChatMessageNewEvent` — WebhookChatMessageNewEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatMessageNewEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `members` — array **(required)**
      - _array of_ `ChannelMember`
        - _(nesting depth limit — see `ChannelMember` in the Schemas appendix)_
    - `users` — array **(required)**
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `message` — Message **(required)**
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `quote` — MessageQuote
        - _(nesting depth limit — see `MessageQuote` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `edit` — boolean
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `latestReactions` — array
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
      - `reactionCounts` — ReactionCounts
        - _(nesting depth limit — see `ReactionCounts` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- `WebhookChatMessageUpdatedEvent` — WebhookChatMessageUpdatedEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatMessageUpdatedOrDeletedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `message` — Message **(required)**
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `quote` — MessageQuote
        - _(nesting depth limit — see `MessageQuote` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `edit` — boolean
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `latestReactions` — array
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
      - `reactionCounts` — ReactionCounts
        - _(nesting depth limit — see `ReactionCounts` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- `WebhookChatMessageDeletedEvent` — WebhookChatMessageDeletedEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatMessageUpdatedOrDeletedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `message` — Message **(required)**
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `quote` — MessageQuote
        - _(nesting depth limit — see `MessageQuote` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `edit` — boolean
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `latestReactions` — array
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
      - `reactionCounts` — ReactionCounts
        - _(nesting depth limit — see `ReactionCounts` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
- `WebhookChatReactionNewEvent` — WebhookChatReactionNewEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatReactionNewOrDeletedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `message` — Message **(required)**
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `quote` — MessageQuote
        - _(nesting depth limit — see `MessageQuote` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `edit` — boolean
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `latestReactions` — array
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
      - `reactionCounts` — ReactionCounts
        - _(nesting depth limit — see `ReactionCounts` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `reaction` — Reaction **(required)**
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
- `WebhookChatReactionDeletedEvent` — WebhookChatReactionDeletedEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatReactionNewOrDeletedEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `message` — Message **(required)**
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `quote` — MessageQuote
        - _(nesting depth limit — see `MessageQuote` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `edit` — boolean
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `latestReactions` — array
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
      - `reactionCounts` — ReactionCounts
        - _(nesting depth limit — see `ReactionCounts` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `reaction` — Reaction **(required)**
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
- `WebhookChatActionTriggeredEvent` — WebhookChatActionTriggeredEvent
  - `id` — string **(required)**
  - `company` — string **(required)**
  - `type` — object **(required)**
  - `time` — number **(required)**
  - `integrationId` — string
  - `botId` — string
  - `data` — WebhookChatActionTriggeredEventData **(required)**
    - `channel` — Channel **(required)**
      - `subject` — string
      - `description` — string
      - `picture` — string — Picture URL
      - `pictureColor` — string — Picture dominant color represented by a hex value.
      - `access` — string _(enum: `private`, `public`)_
      - `company` — string
      - `context` — ChannelContext
        - _(nesting depth limit — see `ChannelContext` in the Schemas appendix)_
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
        - _(nesting depth limit — see `User` in the Schemas appendix)_
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
    - `message` — Message **(required)**
      - `text` — string _(minLen=1; maxLen=5000)_
      - `elements` — array
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `quote` — MessageQuote
        - _(nesting depth limit — see `MessageQuote` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `whatsapp` — boolean
      - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
      - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
      - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
      - `sms` — boolean
      - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
      - `markdown` — boolean
      - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `silent` — boolean
      - `event` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `edit` — boolean
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `latestReactions` — array
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
      - `reactionCounts` — ReactionCounts
        - _(nesting depth limit — see `ReactionCounts` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
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
    - `actionId` — string **(required)**
    - `triggerId` — string **(required)**

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

**`FileNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`ForbiddenExceptionResponseContent`**

- `message` — string **(required)**

**`GetActionTriggerResultResponseContent`**

- `status` — string **(required)** _(enum: `completed`, `pending`)_
- `result` — ActionTriggerResult
  - `url` — string _(minLen=3; maxLen=2048)_

**`GetChannelMemberResponseContent`**

- `member` — ChannelMember **(required)**
  - `id` — string **(required)**
  - `createdAt` — string **(required)**
  - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`GetChannelResponseContent`**

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

**`GetDirectChannelIdRequestContent`**

- `memberId` — string — A User ID of the member to connect with the direct channel. _(minLen=12; maxLen=12)_
- `memberToInvite` — UserToInvite
  - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
  - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.

**`GetDirectChannelIdResponseContent`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`GetFilePresignedDownloadUrlResponseContent`**

- `presignedDownloadUrl` — string **(required)** — The presigned URL for downloading the file.

**`GetInboxStateResponseContent`**

- `channels` — InboxChannelsState **(required)**
  - `unread` — array **(required)**
    - _array of_ `InboxUnreadChannel`
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `unreadAt` — string **(required)** — A date when unread indicator was set by the user.
      - `messageId` — string _(minLen=32; maxLen=32)_
  - `pinned` — array **(required)**
    - _array of_ `InboxPinnedChannel`
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `pinnedAt` — string **(required)**
  - `tagged` — array **(required)**
    - _array of_ `InboxTaggedChannel`
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `tagId` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
- `tags` — array **(required)**
  - _array of_ `InboxTag`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
    - `name` — string **(required)** _(minLen=1; maxLen=80)_

**`GetMessageResponseContent`**

- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`GetMessagingChannelIdRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `senderId` — string — The business sender the conversation runs from: the brand id on RCS, where it is required and is part of the channel id, so two brands never share a conversation with one person. Messenger and Instagram do not read it. The grammar classound and kite enforce for a brand id. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_

**`GetMessagingChannelIdResponseContent`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`GetOrCreateDirectChannelRequestContent`**

- `memberId` — string — A User ID of the member to connect with the direct channel. _(minLen=12; maxLen=12)_
- `memberToInvite` — UserToInvite
  - `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
  - `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
  - `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
  - `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.

**`GetOrCreateDirectChannelResponseContent`**

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

**`GetOrCreateMessagingChannelRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- `channel` — string **(required)** — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `senderId` — string — The business sender the conversation runs from: the brand id on RCS, where it is required and is part of the channel id, so two brands never share a conversation with one person. Messenger and Instagram do not read it. The grammar classound and kite enforce for a brand id. _(pattern=^[A-Za-z0-9_.-]{1,64}$)_
- `outgoing` — boolean — Indicates if the channel is outgoing. It's prevents applying routing settings for the channel. This parameter will be reset to false after 48 hours. Default is false.

**`GetOrCreateMessagingChannelResponseContent`**

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

**`GetOrCreateSmsChannelRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- `outgoing` — boolean — Indicates if the channel is outgoing. It's prevents applying routing settings for the channel. This parameter will be reset to false after 48 hours. Default is false.

**`GetOrCreateSmsChannelResponseContent`**

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

**`GetOrCreateTelephonyChannelRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.

**`GetOrCreateTelephonyChannelResponseContent`**

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

**`GetOrCreateWhatsAppChannelRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.
- `outgoing` — boolean — Indicates if the channel is outgoing. It's prevents applying routing settings for the channel. This parameter will be reset to false after 48 hours. Default is false.

**`GetOrCreateWhatsAppChannelResponseContent`**

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

**`GetSmsChannelIdRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.

**`GetSmsChannelIdResponseContent`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`GetTelephonyChannelIdRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.

**`GetTelephonyChannelIdResponseContent`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`GetTokenResponseContent`**

- `token` — string **(required)** — An authorization token.
- `expires` — number **(required)** — A token's expiration time.

**`GetUploadedFileInfoResponseContent`**

- `file` — MessageAttachment **(required)**
  - `id` — string **(required)**
  - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
  - `mime` — string
  - `name` — string **(required)**
  - `size` — number **(required)**
  - `width` — number
  - `height` — number
  - `thumbnail` — string

**`GetWhatsAppChannelIdRequestContent`**

- `serviceUri` — string **(required)** — The unique identifier of the telephony channel.
- `recipientId` — string — The unique identifier of the recipient. Required if recipientNumber is not provided. _(minLen=12; maxLen=12)_
- `recipientNumber` — string — The unique identifier of the recipient. Required if recipientId is not provided.

**`GetWhatsAppChannelIdResponseContent`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`GroupChannelCreationEventType`**

_Defines which system event is emitted when a group channel is created._

- string _(enum: `conversation_created`, `conversation_created_with_name`)_

**`GroupChannelUnsetOptions`**

- string _(enum: `subject`, `description`, `picture`, `pictureColor`, `access`, `broadcast`, `context`, `contextPtt`, `contextEvents`, `whatsappStatus`, `messagingStatus`, `kiteAssign`, … (+6))_

**`InboxChannelsState`**

- `unread` — array **(required)**
  - _array of_ `InboxUnreadChannel`
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `unreadAt` — string **(required)** — A date when unread indicator was set by the user.
    - `messageId` — string _(minLen=32; maxLen=32)_
- `pinned` — array **(required)**
  - _array of_ `InboxPinnedChannel`
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `pinnedAt` — string **(required)**
- `tagged` — array **(required)**
  - _array of_ `InboxTaggedChannel`
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `tagId` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_

**`InboxPinnedChannel`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `pinnedAt` — string **(required)**

**`InboxTag`**

- `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
- `name` — string **(required)** _(minLen=1; maxLen=80)_

**`InboxTaggedChannel`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `tagId` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_

**`InboxUnreadChannel`**

- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `unreadAt` — string **(required)** — A date when unread indicator was set by the user.
- `messageId` — string _(minLen=32; maxLen=32)_

**`InitialMessage`**

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
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `quote` — MessageQuote
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `text` — string _(minLen=1; maxLen=5000)_
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `mentions` — array
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
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
- `sms` — boolean
- `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
- `markdown` — boolean
- `messageId` — string **(required)** — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
- `mentions` — array — A list of user IDs mentioned in the message.
  - _array of_ `string`

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

**`JoinChannelRequestContent`**

- `silent` — boolean — Set to true to suppress system messages that the user joined the channel. Default is false.

**`JoinChannelResponseContent`**

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

**`LeaveChannelRequestContent`**

- `silent` — boolean — Set to true to suppress system messages that the user left the channel. Default is false.

**`ListChannelMembersReadStatusResponseContent`**

- `members` — array **(required)** — Read status of members.
  - _array of_ `ChannelMemberReadStatus`
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
    - `lastRead` — string
    - `lastReadMessageId` — string

**`ListChannelMembersResponseContent`**

- `members` — array **(required)** — The list of members matching the query.
  - _array of_ `ChannelMember`
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
- `users` — array **(required)** — The list of users matching the query
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

**`ListChannelsResponseContent`**

- `channels` — array **(required)** — A list of channels associated with the user.
  - _array of_ `Channel`
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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

**`ListInboxTaggedChannelsResponseContent`**

- `channels` — array **(required)**
  - _array of_ `InboxTaggedChannel`
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `tagId` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_

**`ListInboxTagsResponseContent`**

- `tags` — array **(required)**
  - _array of_ `InboxTag`
    - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
    - `name` — string **(required)** _(minLen=1; maxLen=80)_

**`ListMessageReactionsResponseContent`**

- `reactions` — array **(required)** — A list of reactions to the specified message.
  - _array of_ `Reaction`
    - `type` — string
    - `userId` — string _(minLen=12; maxLen=12)_
    - `messageId` — string
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

**`ListMessagesResponseContent`**

- `messages` — array **(required)** — A list of messages from the specified channel.
  - _array of_ `Message`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`ListPinnedMessagesResponseContent`**

- `messages` — array **(required)** — A list of pinned messages in the channel.
  - _array of_ `Message`
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`MarkUnreadRequestContent`**

- `messageId` — string — A Message ID in the channel from which to calculate the amount of unread messages. _(minLen=32; maxLen=32)_

**`MemberAlreadyExistExceptionResponseContent`**

- `message` — string **(required)**

**`MemberDeactivatedExceptionResponseContent`**

- `message` — string **(required)**

**`MemberNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`Message`**

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
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `quote` — MessageQuote
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `text` — string _(minLen=1; maxLen=5000)_
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `mentions` — array
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
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
- `sms` — boolean
- `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
- `markdown` — boolean
- `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
- `giphy` — MessageGiphy
  - `id` — string **(required)** _(minLen=1)_
  - `size` — string **(required)** _(pattern=^\d+$)_
  - `url` — string **(required)** _(minLen=1)_
  - `height` — string **(required)** _(pattern=^\d+$)_
  - `width` — string **(required)** _(pattern=^\d+$)_
- `silent` — boolean
- `event` — string
- `messageId` — string **(required)** _(minLen=32; maxLen=32)_
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
- `edit` — boolean
- `mentions` — array
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
- `latestReactions` — array
  - _array of_ `Reaction`
    - `type` — string
    - `userId` — string _(minLen=12; maxLen=12)_
    - `messageId` — string
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
- `reactionCounts` — ReactionCounts
  - _map of_ `number`
- `createdAt` — string **(required)**
- `updatedAt` — string

**`MessageActionNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`MessageAttachment`**

- `id` — string **(required)**
- `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
- `mime` — string
- `name` — string **(required)**
- `size` — number **(required)**
- `width` — number
- `height` — number
- `thumbnail` — string

**`MessageForward`**

- `forwardCompany` — string
- `forwardDate` — string **(required)**
- `forwardEmail` — string
- `forwardName` — string
- `messageId` — string **(required)** _(minLen=32; maxLen=32)_
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_

**`MessageGiphy`**

- `id` — string **(required)** _(minLen=1)_
- `size` — string **(required)** _(pattern=^\d+$)_
- `url` — string **(required)** _(minLen=1)_
- `height` — string **(required)** _(pattern=^\d+$)_
- `width` — string **(required)** _(pattern=^\d+$)_

**`MessageMessagingStatus`**

_The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier._

- string _(enum: `trying`, `sent`, `error`, `delivered`)_

**`MessageNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`MessageQuote`**

- `messageId` — string **(required)** _(minLen=32; maxLen=32)_
- `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
- `text` — string _(minLen=1; maxLen=5000)_
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `mentions` — array
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
- `giphy` — MessageGiphy
  - `id` — string **(required)** _(minLen=1)_
  - `size` — string **(required)** _(pattern=^\d+$)_
  - `url` — string **(required)** _(minLen=1)_
  - `height` — string **(required)** _(pattern=^\d+$)_
  - `width` — string **(required)** _(pattern=^\d+$)_
- `createdAt` — string **(required)**
- `updatedAt` — string

**`MessageSmsStatus`**

- string _(enum: `sent`, `delivered`, `trying`, `error`)_

**`MessageTemplateConfig`**

- `whatsapp` — TemplateWithParameters
  - `name` — string **(required)**
  - `parameters` — array
    - _array of_ `TemplateParameter`
      - `name` — string **(required)**
      - `value` — string **(required)**

**`MessageType`**

- string _(enum: `regular`, `system`, `deleted`)_

**`MessageUnsetFields`**

_The message fields a PartialUpdateMessage may clear. There is deliberately no MESSAGING_CHANNEL or MESSAGING_STATUS member, although the channel enum GroupChannelUnsetOptions did gain MESSAGING_STATUS. Nothing clears a messaging channel message state: kite only ever overwrites it, TRYING to SENT to DELIVERED or ERROR, while the channel state is genuinely cleared on every inbound message. A member added here before something sends it would also be wrong on the wire rather than merely unused: the conversations handler maps each camelCase member to its GetStream key by hand and falls through to the member's own spelling, so an unmapped MESSAGING_STATUS would unset messagingStatus instead of messaging_status and report a success that cleared nothing._

- string _(enum: `text`, `mentions`, `elements`, `attachments`, `quote`, `forward`, `whatsapp`, `whatsappStatus`, `sms`, `smsStatus`)_

**`MessageWhatsAppStatus`**

- string _(enum: `trying`, `sent`, `delivered`, `error`)_

**`MessagingChannel`**

_A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number._

- string _(enum: `messenger`, `instagram`, `rcs`)_

**`MultipleMembersJoinedSystemMessage`**

- `addedMembers` — array **(required)**
  - _array of_ `string`

**`PartialUpdateChannelRequestContent`**

- `silent` — boolean — Set to true to suppress system messages about the updates. Default is false.
- `set` — PartialUpdateChannelSetOptions
  - `subject` — string — The subject of the channel. _(minLen=1; maxLen=80)_
  - `description` — string — The description of the channel. _(maxLen=160)_
  - `picture` — string — The URL of the channel's picture. _(pattern=^https://[^\s/$.?#].[^\s]*$)_
  - `pictureColor` — string — The dominant color of the channel's picture, represented by a hex value. _(pattern=^#[0-9a-fA-F]{6}$)_
  - `access` — string _(enum: `private`, `public`)_
  - `broadcast` — boolean — Indicates if the channel is broadcast-only. Default is false.
  - `context` — ChannelContext
    - `source` — string _(enum: `kite`)_
    - `target` — string
    - `events` — array
      - _array of_ `ChannelContextEvent`
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
    - `ptt` — ChannelContextPushToTalk
      - `broadcastId` — string — A unique identifier of x-hoppers broadcast conference. If present x-hoppers application will use broadcast and push-to-talk functionality for the channel.
  - `whatsappStatus` — string _(enum: `24h_channel_closed`)_
  - `sms` — boolean — Indicates if the channel supports SMS. Default is false.
  - `mms` — boolean — Indicates if the channel supports MMS. Default is false.
  - `whatsapp` — boolean — Indicates if the channel supports WhatsApp. Default is false.
  - `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
  - `messagingSenderId` — string — The business side of the conversation: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. A reply has to name the sender it is sent from. On Messenger and Instagram kite writes it from the inbound event, because the channel id hashes the sender's linked service and not the sender; on RCS the channel id includes the brand, and it is written when the channel is created.
  - `messagingReplyUntil` — number — Epoch seconds until which a reply still reaches the person. On Messenger and Instagram this is Meta's 7 day HUMAN_AGENT deadline, restarted by each inbound message; classound applies the tag itself, so this is the one deadline a client has to show. 0 means the deadline is not known, which is what the inbound event carries when the session row was gone before it could be read back; it does not mean the window has closed, so a client reads the window as closed on `messagingReplyUntil > 0 && now > messagingReplyUntil` and shows nothing at 0. Absent on a channel with no reply window.
  - `kiteAssign` — string — The unique identifier of the assignee.
  - `serviceTitle` — string
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
  - `autoRecord` — boolean
  - `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
  - `transcriptionLanguage` — string
  - `wizyGuestViewOnly` — boolean
- `unset` — array — Options to unset specific fields in the channel.
  - _array of_ `GroupChannelUnsetOptions`

**`PartialUpdateChannelResponseContent`**

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

**`PartialUpdateChannelSetOptions`**

- `subject` — string — The subject of the channel. _(minLen=1; maxLen=80)_
- `description` — string — The description of the channel. _(maxLen=160)_
- `picture` — string — The URL of the channel's picture. _(pattern=^https://[^\s/$.?#].[^\s]*$)_
- `pictureColor` — string — The dominant color of the channel's picture, represented by a hex value. _(pattern=^#[0-9a-fA-F]{6}$)_
- `access` — string _(enum: `private`, `public`)_
- `broadcast` — boolean — Indicates if the channel is broadcast-only. Default is false.
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
- `whatsappStatus` — string _(enum: `24h_channel_closed`)_
- `sms` — boolean — Indicates if the channel supports SMS. Default is false.
- `mms` — boolean — Indicates if the channel supports MMS. Default is false.
- `whatsapp` — boolean — Indicates if the channel supports WhatsApp. Default is false.
- `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
- `messagingSenderId` — string — The business side of the conversation: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. A reply has to name the sender it is sent from. On Messenger and Instagram kite writes it from the inbound event, because the channel id hashes the sender's linked service and not the sender; on RCS the channel id includes the brand, and it is written when the channel is created.
- `messagingReplyUntil` — number — Epoch seconds until which a reply still reaches the person. On Messenger and Instagram this is Meta's 7 day HUMAN_AGENT deadline, restarted by each inbound message; classound applies the tag itself, so this is the one deadline a client has to show. 0 means the deadline is not known, which is what the inbound event carries when the session row was gone before it could be read back; it does not mean the window has closed, so a client reads the window as closed on `messagingReplyUntil > 0 && now > messagingReplyUntil` and shows nothing at 0. Absent on a channel with no reply window.
- `kiteAssign` — string — The unique identifier of the assignee.
- `serviceTitle` — string
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
- `autoRecord` — boolean
- `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
- `transcriptionLanguage` — string
- `wizyGuestViewOnly` — boolean

**`PartialUpdateMessageRequestContent`**

- `set` — PartialUpdateMessageSetInput
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `mentions` — array — A list of user IDs mentioned in the message.
    - _array of_ `string`
- `unset` — array — Fields to unset during the partial update.
  - _array of_ `MessageUnsetFields`
- `silent` — boolean — Set to true to suppress the updated indicator. Defaults to false.

**`PartialUpdateMessageResponseContent`**

- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`PartialUpdateMessageSetInput`**

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
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `quote` — MessageQuote
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `text` — string _(minLen=1; maxLen=5000)_
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `mentions` — array
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
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
- `sms` — boolean
- `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
- `markdown` — boolean
- `mentions` — array — A list of user IDs mentioned in the message.
  - _array of_ `string`

**`PinMessageRequestContent`**

- `expiresAfter` — number — The duration in seconds after which the pinned message will be automatically unpinned. If neither `expiresAfter` nor `expiresAt` is provided, the message will remain pinned indefinitely. Providing both `expiresAfter` and `expiresAt` will result in a validation error.
- `expiresAt` — string — The specific date and time (in ISO 8601 format) when the pinned message will be automatically unpinned. If neither `expiresAfter` nor `expiresAt` is provided, the message will remain pinned indefinitely. Providing both `expiresAfter` and `expiresAt` will result in a validation error.
- `silent` — boolean — Set to true to suppress system messages generated by this operation. Defaults to false.

**`QueryChannelsRequestContent`**

- `query` — ChannelsQuery
  - `ids` — array _(maxItems=30)_
    - _array of_ `string`

**`QueryChannelsResponseContent`**

- `channels` — array **(required)** — A list of channels matched the query.
  - _array of_ `Channel`
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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

**`RateLimitExceededExceptionResponseContent`**

- `message` — string **(required)** _(default=Too Many Requests)_

**`Reaction`**

- `type` — string
- `userId` — string _(minLen=12; maxLen=12)_
- `messageId` — string
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

**`ReactionCounts`**

- _map of_ `number`

**`ReactionType`**

- string _(enum: `thumbsup`, `clap`, `slightly_smiling_face`, `smiley`, `heart`, `eyes`, `white_check_mark`, `confused`, `thumbsdown`)_

**`ScheduleExternalFlagAdjustmentJobRequestContent`**

- `userId` — string **(required)** — The unique identifier of the user. _(minLen=12; maxLen=12)_

**`SendActionTriggerResultRequestContent`**

- `status` — string **(required)** _(enum: `completed`, `pending`)_
- `result` — ActionTriggerResult **(required)**
  - `url` — string _(minLen=3; maxLen=2048)_

**`SendGiphyRequestContent`**

- `messageId` — string — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
- `giphy` — MessageGiphy **(required)**
  - `id` — string **(required)** _(minLen=1)_
  - `size` — string **(required)** _(pattern=^\d+$)_
  - `url` — string **(required)** _(minLen=1)_
  - `height` — string **(required)** _(pattern=^\d+$)_
  - `width` — string **(required)** _(pattern=^\d+$)_

**`SendGiphyResponseContent`**

- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`SendMessageReactionRequestContent`**

- `reactionType` — string **(required)** _(enum: `thumbsup`, `clap`, `slightly_smiling_face`, `smiley`, `heart`, `eyes`, `white_check_mark`, `confused`, `thumbsdown`)_

**`SendMessageRequestContent`**

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
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `quote` — MessageQuote
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `text` — string _(minLen=1; maxLen=5000)_
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `mentions` — array
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
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
- `sms` — boolean
- `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
- `markdown` — boolean
- `messageId` — string — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
- `mentions` — array — A list of user IDs mentioned in the message.
  - _array of_ `string`

**`SendMessageResponseContent`**

- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`SendSystemMessageRequestContent`**

- `userId` — string — The unique identifier of the user when a service token is used. _(minLen=12; maxLen=12)_
- `message` — union **(required)**
  - _oneOf_ — exactly one of:
    - **`whatsAppClosed`**
      - `whatsAppClosed` — WhatsAppClosedSystemMessage **(required)**
    - **`multipleMembersJoined`**
      - `multipleMembersJoined` — MultipleMembersJoinedSystemMessage **(required)**
        - `addedMembers` — array **(required)**
          - _array of_ `string`

**`SendSystemMessageResponseContent`**

- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

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

**`SkippedMember`**

- `id` — string — The unique identifier of the skipped user if it is known. _(minLen=12; maxLen=12)_
- `email` — string — The email address of the skipped user if it is known. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string — The phone number of the skipped user if it is known. _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_

**`SystemMessage`**

- _oneOf_ — exactly one of:
  - **`whatsAppClosed`**
    - `whatsAppClosed` — WhatsAppClosedSystemMessage **(required)**
  - **`multipleMembersJoined`**
    - `multipleMembersJoined` — MultipleMembersJoinedSystemMessage **(required)**
      - `addedMembers` — array **(required)**
        - _array of_ `string`

**`TagNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`TargetNotEligibleExceptionResponseContent`**

- `message` — string **(required)**
- `reason` — string _(enum: `no_license`)_

**`TargetNotEligibleReason`**

- string _(enum: `no_license`)_

**`TargetNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`TemplateParameter`**

- `name` — string **(required)**
- `value` — string **(required)**

**`TemplateWithParameters`**

- `name` — string **(required)**
- `parameters` — array
  - _array of_ `TemplateParameter`
    - `name` — string **(required)**
    - `value` — string **(required)**

**`TriggerMessageActionResponseContent`**

- `triggerId` — string **(required)** _(minLen=32; maxLen=32)_

**`TriggerNotFoundExceptionResponseContent`**

- `message` — string **(required)**

**`UntagChannelRequestContent`**

- `tagId` — string **(required)** — The unique identifier of the tag to remove from the channel. _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_

**`UpdateChannelRequestContent`**

- `subject` — string — The subject of the channel. _(minLen=1; maxLen=80)_
- `description` — string — The description of the channel. _(maxLen=160)_
- `picture` — string — The URL of the channel's picture. _(pattern=^https://[^\s/$.?#].[^\s]*$)_
- `pictureColor` — string — The dominant color of the channel's picture, represented by a hex value. _(pattern=^#[0-9a-fA-F]{6}$)_
- `access` — string _(enum: `private`, `public`)_
- `broadcast` — boolean — Indicates if the channel is broadcast-only. Default is false.
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
- `whatsappStatus` — string _(enum: `24h_channel_closed`)_
- `sms` — boolean — Indicates if the channel supports SMS. Default is false.
- `mms` — boolean — Indicates if the channel supports MMS. Default is false.
- `whatsapp` — boolean — Indicates if the channel supports WhatsApp. Default is false.
- `messagingStatus` — string — Set when classound refused a reply because the person's messaging window is closed (a 409 on the send). Unset by the next inbound message, which is the only thing that reopens the window. _(enum: `window_closed`)_
- `messagingSenderId` — string — The business side of the conversation: the Facebook Page ID on Messenger, the Instagram account ID on Instagram, the brand id on RCS. A reply has to name the sender it is sent from. On Messenger and Instagram kite writes it from the inbound event, because the channel id hashes the sender's linked service and not the sender; on RCS the channel id includes the brand, and it is written when the channel is created.
- `messagingReplyUntil` — number — Epoch seconds until which a reply still reaches the person. On Messenger and Instagram this is Meta's 7 day HUMAN_AGENT deadline, restarted by each inbound message; classound applies the tag itself, so this is the one deadline a client has to show. 0 means the deadline is not known, which is what the inbound event carries when the session row was gone before it could be read back; it does not mean the window has closed, so a client reads the window as closed on `messagingReplyUntil > 0 && now > messagingReplyUntil` and shows nothing at 0. Absent on a channel with no reply window.
- `kiteAssign` — string — The unique identifier of the assignee.
- `serviceTitle` — string
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
- `autoRecord` — boolean
- `autoTranscribe` — boolean — Indicates if a conference in the channel starts transcription automatically. When absent, clients follow autoRecord, which used to start both recording and transcription.
- `transcriptionLanguage` — string
- `wizyGuestViewOnly` — boolean
- `silent` — boolean — Set to true to suppress system messages about the updates. Default is false.

**`UpdateChannelResponseContent`**

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

**`UpdateInboxTagRequestContent`**

- `name` — string **(required)** — The name of the tag. _(minLen=1; maxLen=80)_

**`UpdateInboxTagResponseContent`**

- `tag` — InboxTag **(required)**
  - `id` — string **(required)** _(pattern=^[0-9a-z]{6}$; minLen=6; maxLen=6)_
  - `name` — string **(required)** _(minLen=1; maxLen=80)_

**`UpdateMessageRequestContent`**

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
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `quote` — MessageQuote
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `text` — string _(minLen=1; maxLen=5000)_
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `mentions` — array
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
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
- `sms` — boolean
- `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
- `markdown` — boolean
- `mentions` — array — A list of user IDs mentioned in the message.
  - _array of_ `string`
- `silent` — boolean — Set to true to suppress the updated indicator. Defaults to false.

**`UpdateMessageResponseContent`**

- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`UploadFileOptions`**

- `category` — string _(enum: `channels`, `recordings`, `wizyconfRecordings`)_
- `region` — string — The region in which you need to upload the file. It is only for s2s, in other cases it will be ignored.

**`UploadFileRequestContent`**

- `name` — string **(required)** — The name of the file. Unreadable characters will be replaced with underscores. _(minLen=1; maxLen=255)_
- `options` — UploadFileOptions
  - `category` — string _(enum: `channels`, `recordings`, `wizyconfRecordings`)_
  - `region` — string — The region in which you need to upload the file. It is only for s2s, in other cases it will be ignored.

**`UploadFileResponseContent`**

- `fileId` — string **(required)** — The unique identifier of the file.
- `presignedUploadUrl` — string **(required)** — The presigned URL for uploading the file.

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

**`UserToInvite`**

- `email` — string — The email address of the invited user. If no user exists with the specified email and "colleague" flag is provided, the system will retrieve the colleague's details from the PBX. _(pattern=^(^[\w+-]+(\.[\w+-]+)*)@(([\w-]+\.)+\w{2,}$)$)_
- `phone` — string — The phone number of the invited user. This phone number is used to create or find the user if an email address is not provided. On Messenger and Instagram it is not a phone number at all: the caller passes the channel's own customer id, the Page Scoped ID on Messenger, so the identity key stays the one the supplier reports. On RCS it is the person's phone number. A phone number allows up to 17 digits and a Page Scoped ID is 17, so there is no headroom left, and the Instagram scoped id has to be checked against the same limit. A WhatsApp user who hides the number is invited by the BSUID exactly as Meta spells it (see InviteePhone). _(pattern=^(\+?[0-9]{4,17}|[A-Za-z]{2}\.[A-Za-z0-9]{1,128})$)_
- `name` — string — An optional name for the invited user. If the user logs in later and a different name is provided via SSO or the PBX, the system will update the user's name accordingly.
- `colleague` — boolean — A flag to indicate that specified email are registered colleague on the PBX. When provided, the system will search for the colleague on the PBX and automatically establish a connection to the organization if one does not already exist. If the specified colleague does not exist on the WMS, a ValidationException will be thrown and no users will be invited.

**`ValidationExceptionResponseContent`**

- `message` — string **(required)**

**`WebhookChatActionTriggeredEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatActionTriggeredEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
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
  - `actionId` — string **(required)**
  - `triggerId` — string **(required)**

**`WebhookChatActionTriggeredEventData`**

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
- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string
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
- `actionId` — string **(required)**
- `triggerId` — string **(required)**

**`WebhookChatChannelCreatedEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatChannelCreatedOrUpdatedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `members` — array **(required)**
    - _array of_ `ChannelMember`
      - `id` — string **(required)**
      - `createdAt` — string **(required)**
      - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`WebhookChatChannelCreatedOrUpdatedEventData`**

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
- `members` — array **(required)**
  - _array of_ `ChannelMember`
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`WebhookChatChannelUpdatedEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatChannelCreatedOrUpdatedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `members` — array **(required)**
    - _array of_ `ChannelMember`
      - `id` — string **(required)**
      - `createdAt` — string **(required)**
      - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`WebhookChatMemberAddedEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatMemberAddedOrRemovedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `member` — ChannelMember **(required)**
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`WebhookChatMemberAddedOrRemovedEventData`**

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
- `member` — ChannelMember **(required)**
  - `id` — string **(required)**
  - `createdAt` — string **(required)**
  - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`WebhookChatMemberRemovedEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatMemberAddedOrRemovedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `member` — ChannelMember **(required)**
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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

**`WebhookChatMessageDeletedEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatMessageUpdatedOrDeletedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`WebhookChatMessageNewEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatMessageNewEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `members` — array **(required)**
    - _array of_ `ChannelMember`
      - `id` — string **(required)**
      - `createdAt` — string **(required)**
      - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`WebhookChatMessageNewEventData`**

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
- `members` — array **(required)**
  - _array of_ `ChannelMember`
    - `id` — string **(required)**
    - `createdAt` — string **(required)**
    - `role` — string **(required)** _(enum: `member`, `supervisor`)_
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
- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`WebhookChatMessageUpdatedEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatMessageUpdatedOrDeletedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string

**`WebhookChatMessageUpdatedOrDeletedEventData`**

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
- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string

**`WebhookChatReactionDeletedEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatReactionNewOrDeletedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `reaction` — Reaction **(required)**
    - `type` — string
    - `userId` — string _(minLen=12; maxLen=12)_
    - `messageId` — string
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

**`WebhookChatReactionNewEvent`**

- `id` — string **(required)**
- `company` — string **(required)**
- `type` — object **(required)**
- `time` — number **(required)**
- `integrationId` — string
- `botId` — string
- `data` — WebhookChatReactionNewOrDeletedEventData **(required)**
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
        - _(nesting depth limit — see `ChannelContextEvent` in the Schemas appendix)_
      - `ptt` — ChannelContextPushToTalk
        - _(nesting depth limit — see `ChannelContextPushToTalk` in the Schemas appendix)_
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
  - `message` — Message **(required)**
    - `text` — string _(minLen=1; maxLen=5000)_
    - `elements` — array
      - _array of_ `Element`
        - _(nesting depth limit — see `Element` in the Schemas appendix)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `quote` — MessageQuote
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
      - `user` — User **(required)**
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `text` — string _(minLen=1; maxLen=5000)_
      - `attachments` — array
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
      - `forward` — MessageForward
        - _(nesting depth limit — see `MessageForward` in the Schemas appendix)_
      - `mentions` — array
        - _(nesting depth limit — see `User` in the Schemas appendix)_
      - `giphy` — MessageGiphy
        - _(nesting depth limit — see `MessageGiphy` in the Schemas appendix)_
      - `createdAt` — string **(required)**
      - `updatedAt` — string
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `whatsapp` — boolean
    - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
    - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
    - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
    - `sms` — boolean
    - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
    - `markdown` — boolean
    - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `silent` — boolean
    - `event` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `edit` — boolean
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `latestReactions` — array
      - _array of_ `Reaction`
        - _(nesting depth limit — see `Reaction` in the Schemas appendix)_
    - `reactionCounts` — ReactionCounts
      - _map of_ `number`
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `reaction` — Reaction **(required)**
    - `type` — string
    - `userId` — string _(minLen=12; maxLen=12)_
    - `messageId` — string
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

**`WebhookChatReactionNewOrDeletedEventData`**

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
- `message` — Message **(required)**
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
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `quote` — MessageQuote
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
    - `text` — string _(minLen=1; maxLen=5000)_
    - `attachments` — array
      - _array of_ `MessageAttachment`
        - _(nesting depth limit — see `MessageAttachment` in the Schemas appendix)_
    - `forward` — MessageForward
      - `forwardCompany` — string
      - `forwardDate` — string **(required)**
      - `forwardEmail` — string
      - `forwardName` — string
      - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
      - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
    - `mentions` — array
      - _array of_ `User`
        - _(nesting depth limit — see `User` in the Schemas appendix)_
    - `giphy` — MessageGiphy
      - `id` — string **(required)** _(minLen=1)_
      - `size` — string **(required)** _(pattern=^\d+$)_
      - `url` — string **(required)** _(minLen=1)_
      - `height` — string **(required)** _(pattern=^\d+$)_
      - `width` — string **(required)** _(pattern=^\d+$)_
    - `createdAt` — string **(required)**
    - `updatedAt` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `whatsapp` — boolean
  - `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
  - `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
  - `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
  - `sms` — boolean
  - `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
  - `markdown` — boolean
  - `type` — string **(required)** _(enum: `regular`, `system`, `deleted`)_
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `silent` — boolean
  - `event` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `edit` — boolean
  - `mentions` — array
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
  - `latestReactions` — array
    - _array of_ `Reaction`
      - `type` — string
      - `userId` — string _(minLen=12; maxLen=12)_
      - `messageId` — string
      - `user` — User
        - _(nesting depth limit — see `User` in the Schemas appendix)_
  - `reactionCounts` — ReactionCounts
    - _map of_ `number`
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `reaction` — Reaction **(required)**
  - `type` — string
  - `userId` — string _(minLen=12; maxLen=12)_
  - `messageId` — string
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

**`WebhookEventType`**

- string _(enum: `chat:channel:created`, `chat:channel:updated`, `chat:member:added`, `chat:member:removed`, `chat:message:new`, `chat:message:updated`, `chat:message:deleted`, `chat:reaction:new`, `chat:reaction:deleted`, `chat:action:triggered`)_

**`WelcomeMessage`**

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
- `attachments` — array
  - _array of_ `MessageAttachment`
    - `id` — string **(required)**
    - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
    - `mime` — string
    - `name` — string **(required)**
    - `size` — number **(required)**
    - `width` — number
    - `height` — number
    - `thumbnail` — string
- `quote` — MessageQuote
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
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
  - `text` — string _(minLen=1; maxLen=5000)_
  - `attachments` — array
    - _array of_ `MessageAttachment`
      - `id` — string **(required)**
      - `fsId` — string **(required)** — This *is* documentation about the field. Describe here what fsId and how to get it.
      - `mime` — string
      - `name` — string **(required)**
      - `size` — number **(required)**
      - `width` — number
      - `height` — number
      - `thumbnail` — string
  - `forward` — MessageForward
    - `forwardCompany` — string
    - `forwardDate` — string **(required)**
    - `forwardEmail` — string
    - `forwardName` — string
    - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
    - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
  - `mentions` — array
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
  - `giphy` — MessageGiphy
    - `id` — string **(required)** _(minLen=1)_
    - `size` — string **(required)** _(pattern=^\d+$)_
    - `url` — string **(required)** _(minLen=1)_
    - `height` — string **(required)** _(pattern=^\d+$)_
    - `width` — string **(required)** _(pattern=^\d+$)_
  - `createdAt` — string **(required)**
  - `updatedAt` — string
- `forward` — MessageForward
  - `forwardCompany` — string
  - `forwardDate` — string **(required)**
  - `forwardEmail` — string
  - `forwardName` — string
  - `messageId` — string **(required)** _(minLen=32; maxLen=32)_
  - `channelId` — string **(required)** — Direct-channel ids are the 8-4-4-4-8 slices of the two member ids. An `a_` member id puts `_` in a slice, so the pattern allows it. _(pattern=^[0-9a-z_]{8}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{4}\b-[0-9a-z_]{8}$; minLen=32; maxLen=32)_
- `whatsapp` — boolean
- `whatsappStatus` — string _(enum: `trying`, `sent`, `delivered`, `error`)_
- `messagingChannel` — string — A customer messaging channel that reaches x-bees through classound and is not SMS or WhatsApp. One discriminator instead of a boolean per channel, so a new channel adds a member here and not a set of channel fields. An RCS conversation is not a telephony channel, and its customer id is the person's phone number. _(enum: `messenger`, `instagram`, `rcs`)_
- `messagingStatus` — string — The delivery state of a message an x-bees user sent over a customer messaging channel (see MessagingChannel), the same four states as WhatsApp. TRYING, SENT and ERROR are written by kite around the send; DELIVERED and a late ERROR arrive through the channel's status stream event (MESSENGER.STATUS, RCS.STATUS). A READ report is recorded as DELIVERED, as the WhatsApp producer does one hop earlier. _(enum: `trying`, `sent`, `error`, `delivered`)_
- `sms` — boolean
- `smsStatus` — string _(enum: `sent`, `delivered`, `trying`, `error`)_
- `markdown` — boolean
- `messageId` — string **(required)** — The unique identifier of the message. If not provided, an ID will be auto-generated. _(minLen=32; maxLen=32)_
- `mentions` — array — A list of user IDs mentioned in the message.
  - _array of_ `string`
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

**`WhatsAppClosedSystemMessage`**

- WhatsAppClosedSystemMessage

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
