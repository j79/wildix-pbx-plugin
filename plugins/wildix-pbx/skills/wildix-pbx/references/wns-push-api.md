## WNS Push API

_OpenAPI: Push notifications — version —_

**Servers**

- `https://notifications.wildix.com` — Production
- `https://notifications-stable.wildix.com` — Stable
- `https://notifications-stage.wildix.com` — Stage

### Push

#### `POST` `/api/v2/push/call`

Send push call notification operation

- operationId: `SendPushCall`
- **Request body** (`application/json` — `SendPushCallRequestContent`) **(required)**
  - `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
  - `token` — string **(required)** — Device token _(minLen=1)_
  - `event` — string **(required)** _(enum: `call`, `missed-call`, `cancelled`)_
  - `lang` — string — Receiver language _(default=en)_
  - `fromNumber` — string — Sender extension _(default=)_
  - `fromName` — string — Sender name _(default=)_
  - `toNumber` — string — Receiver extension _(default=)_
  - `domain` — string — PBX domain _(default=)_
  - `sound` — string — Custom call sound _(default=)_
  - `id` — string — Call ID _(default=)_
- **Response 200** (`SendPushCallResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — SendPushCallResult **(required)**
    - `messageId` — string
- Errors: `400`

#### `PUT` `/api/v2/push/endpoint`

Create endpoint for sending push notification

- operationId: `CreateEndpoint`
- **Request body** (`application/json` — `CreateEndpointRequestContent`) **(required)**
  - `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
  - `token` — string **(required)** — Device token _(minLen=1)_
  - `event` — string **(required)** _(enum: `message`, `group-chat`, `call`, `missed-call`, `cancelled`, `ptt`)_
- **Response 200** (`CreateEndpointResponseContent`)
  - `result` — CreateEndpointResult **(required)**
    - `endpointArn` — string
  - `type` — string **(required)** _(enum: `result`, `error`)_
- Errors: `400`

#### `DELETE` `/api/v2/push/endpoint`

Delete endpoint

- operationId: `DeleteEndpoint`
- **Parameters**
  - `arn` (query) — string **(required)** — Endpoint ARN _(minLen=1)_
- **Response 200** (`DeleteEndpointResponseContent`)
  - `result` — boolean **(required)**
  - `type` — string **(required)** _(enum: `result`, `error`)_
- Errors: `400`

#### `POST` `/api/v2/push/message`

Send push message notification operation

- operationId: `SendPushMessage`
- **Request body** (`application/json` — `SendPushMessageRequestContent`) **(required)**
  - `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
  - `token` — string **(required)** — Device token _(minLen=1)_
  - `message` — string — Message content _(default=)_
  - `lang` — string — Receiver language _(default=en)_
  - `fromNumber` — string — Sender extension _(default=)_
  - `fromName` — string — Sender name _(default=)_
  - `toNumber` — string — Receiver extension _(default=)_
  - `toName` — string — Receiver name _(default=)_
  - `domain` — string — PBX domain _(default=)_
  - `missed` — string — Amount of missed messages _(default=)_
  - `roomName` — string — Room name of group chat _(default=)_
  - `roomJid` — string — Room jid of group chat _(default=)_
  - `sequence` — string — Sequence of message _(default=)_
  - `id` — string — Message ID
- **Response 200** (`SendPushMessageResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — SendPushMessageResult **(required)**
    - `messageId` — string
- Errors: `400`

#### `POST` `/api/v2/push/messages`

Batch sending of push messages

- operationId: `SendPushMessages`
- **Request body** (`application/json` — `SendPushMessagesRequestContent`) **(required)**
  - `messages` — array **(required)**
    - _array of_ `SendPushGroupMessageInput`
      - `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
      - `token` — string **(required)** — Device token _(minLen=1)_
      - `message` — string — Message content _(default=)_
      - `lang` — string — Receiver language _(default=en)_
      - `fromNumber` — string — Sender extension _(default=)_
      - `fromName` — string — Sender name _(default=)_
      - `toNumber` — string — Receiver extension _(default=)_
      - `toName` — string — Receiver name _(default=)_
      - `domain` — string — PBX domain _(default=)_
      - `missed` — string — Amount of missed messages _(default=)_
      - `roomName` — string — Room name of group chat _(default=)_
      - `roomJid` — string — Room jid of group chat _(default=)_
      - `sequence` — string — Sequence of message _(default=)_
      - `id` — string — Message ID
- **Response 200** (`SendPushMessagesResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — array **(required)**
    - _array of_ `BatchResultItem`
      - `messageId` — string
      - `status` — string
- Errors: `400`

#### `POST` `/api/v2/push/ptt`

Send PTT push notification operation

- operationId: `SendPushPtt`
- **Request body** (`application/json` — `SendPushPttRequestContent`) **(required)**
  - `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
  - `token` — string **(required)** — Device token _(minLen=1)_
  - `fromNumber` — string **(required)** — User extension _(minLen=1)_
  - `fromName` — string **(required)** — User name _(minLen=1)_
  - `url` — string **(required)** — File URL to download _(minLen=1)_
  - `conferenceId` — string **(required)** — Conference id _(minLen=1)_
- **Response 200** (`SendPushPttResponseContent`)
  - `type` — string **(required)** _(enum: `result`, `error`)_
  - `result` — SendPushPttResult **(required)**
    - `messageId` — string
- Errors: `400`

### Schemas appendix — WNS Push API

<details><summary>22 component schemas</summary>

**`BadRequestErrorResponseContent`**

- `reason` — string **(required)**
- `type` — object **(required)**

**`BatchResultItem`**

- `messageId` — string
- `status` — string

**`CreateEndpointRequestContent`**

- `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
- `token` — string **(required)** — Device token _(minLen=1)_
- `event` — string **(required)** _(enum: `message`, `group-chat`, `call`, `missed-call`, `cancelled`, `ptt`)_

**`CreateEndpointResponseContent`**

- `result` — CreateEndpointResult **(required)**
  - `endpointArn` — string
- `type` — string **(required)** _(enum: `result`, `error`)_

**`CreateEndpointResult`**

- `endpointArn` — string

**`DeleteEndpointResponseContent`**

- `result` — boolean **(required)**
- `type` — string **(required)** _(enum: `result`, `error`)_

**`PushCallEvent`**

- string _(enum: `call`, `missed-call`, `cancelled`)_

**`PushEvent`**

- string _(enum: `message`, `group-chat`, `call`, `missed-call`, `cancelled`, `ptt`)_

**`PushType`**

- string _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_

**`ResponseType`**

- string _(enum: `result`, `error`)_

**`SendPushCallRequestContent`**

- `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
- `token` — string **(required)** — Device token _(minLen=1)_
- `event` — string **(required)** _(enum: `call`, `missed-call`, `cancelled`)_
- `lang` — string — Receiver language _(default=en)_
- `fromNumber` — string — Sender extension _(default=)_
- `fromName` — string — Sender name _(default=)_
- `toNumber` — string — Receiver extension _(default=)_
- `domain` — string — PBX domain _(default=)_
- `sound` — string — Custom call sound _(default=)_
- `id` — string — Call ID _(default=)_

**`SendPushCallResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — SendPushCallResult **(required)**
  - `messageId` — string

**`SendPushCallResult`**

- `messageId` — string

**`SendPushGroupMessageInput`**

- `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
- `token` — string **(required)** — Device token _(minLen=1)_
- `message` — string — Message content _(default=)_
- `lang` — string — Receiver language _(default=en)_
- `fromNumber` — string — Sender extension _(default=)_
- `fromName` — string — Sender name _(default=)_
- `toNumber` — string — Receiver extension _(default=)_
- `toName` — string — Receiver name _(default=)_
- `domain` — string — PBX domain _(default=)_
- `missed` — string — Amount of missed messages _(default=)_
- `roomName` — string — Room name of group chat _(default=)_
- `roomJid` — string — Room jid of group chat _(default=)_
- `sequence` — string — Sequence of message _(default=)_
- `id` — string — Message ID

**`SendPushMessageRequestContent`**

- `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
- `token` — string **(required)** — Device token _(minLen=1)_
- `message` — string — Message content _(default=)_
- `lang` — string — Receiver language _(default=en)_
- `fromNumber` — string — Sender extension _(default=)_
- `fromName` — string — Sender name _(default=)_
- `toNumber` — string — Receiver extension _(default=)_
- `toName` — string — Receiver name _(default=)_
- `domain` — string — PBX domain _(default=)_
- `missed` — string — Amount of missed messages _(default=)_
- `roomName` — string — Room name of group chat _(default=)_
- `roomJid` — string — Room jid of group chat _(default=)_
- `sequence` — string — Sequence of message _(default=)_
- `id` — string — Message ID

**`SendPushMessageResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — SendPushMessageResult **(required)**
  - `messageId` — string

**`SendPushMessageResult`**

- `messageId` — string

**`SendPushMessagesRequestContent`**

- `messages` — array **(required)**
  - _array of_ `SendPushGroupMessageInput`
    - `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
    - `token` — string **(required)** — Device token _(minLen=1)_
    - `message` — string — Message content _(default=)_
    - `lang` — string — Receiver language _(default=en)_
    - `fromNumber` — string — Sender extension _(default=)_
    - `fromName` — string — Sender name _(default=)_
    - `toNumber` — string — Receiver extension _(default=)_
    - `toName` — string — Receiver name _(default=)_
    - `domain` — string — PBX domain _(default=)_
    - `missed` — string — Amount of missed messages _(default=)_
    - `roomName` — string — Room name of group chat _(default=)_
    - `roomJid` — string — Room jid of group chat _(default=)_
    - `sequence` — string — Sequence of message _(default=)_
    - `id` — string — Message ID

**`SendPushMessagesResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — array **(required)**
  - _array of_ `BatchResultItem`
    - `messageId` — string
    - `status` — string

**`SendPushPttRequestContent`**

- `type` — string **(required)** _(enum: `android`, `rnc.android`, `xhoppers.android`, `collaboration.android`, `ios`, `rnc.ios`, `xhoppers.ios`, `collaboration.ios`, `chrome`, `rnc.chrome`, `xhoppers.chrome`, `collaboration.chrome`)_
- `token` — string **(required)** — Device token _(minLen=1)_
- `fromNumber` — string **(required)** — User extension _(minLen=1)_
- `fromName` — string **(required)** — User name _(minLen=1)_
- `url` — string **(required)** — File URL to download _(minLen=1)_
- `conferenceId` — string **(required)** — Conference id _(minLen=1)_

**`SendPushPttResponseContent`**

- `type` — string **(required)** _(enum: `result`, `error`)_
- `result` — SendPushPttResult **(required)**
  - `messageId` — string

**`SendPushPttResult`**

- `messageId` — string

</details>
